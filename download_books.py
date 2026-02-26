import os
import re
import time
import urllib.request
import urllib.error
import urllib.parse
from html.parser import HTMLParser

def get_html(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            return response.read().decode('utf-8', errors='replace')
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return ""

class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_booklink = False
        self.in_link = False
        self.in_title = False
        self.in_subtitle = False
        
        self.current_href = None
        self.current_title = ""
        self.current_subtitle = ""
        
        self.books = []
        self.next_page = None

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        
        if tag == 'li' and attr_dict.get('class') == 'booklink':
            self.in_booklink = True
            self.current_href = None
            self.current_title = ""
            self.current_subtitle = ""
            
        elif tag == 'a' and self.in_booklink and attr_dict.get('class') == 'link':
            self.in_link = True
            self.current_href = attr_dict.get('href')
            
        elif tag == 'span' and self.in_link:
            cls = attr_dict.get('class')
            if cls == 'title':
                self.in_title = True
            elif cls == 'subtitle':
                self.in_subtitle = True
                
        elif tag == 'a' and attr_dict.get('title') == 'Go to the next page of results.':
            self.next_page = attr_dict.get('href')

    def handle_endtag(self, tag):
        if tag == 'span':
            self.in_title = False
            self.in_subtitle = False
        elif tag == 'a' and self.in_link:
            self.in_link = False
            if self.current_href and self.current_title:
                self.books.append({
                    'href': self.current_href,
                    'title': self.current_title.strip(),
                    'author': self.current_subtitle.strip()
                })
        elif tag == 'li' and self.in_booklink:
            self.in_booklink = False

    def handle_data(self, data):
        if self.in_title:
            self.current_title += data
        elif self.in_subtitle:
            self.current_subtitle += data

class BookPageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.txt_url = None
        
    def handle_starttag(self, tag, attrs):
        if self.txt_url:
            return
        attr_dict = dict(attrs)
        if tag == 'a':
            t = attr_dict.get('type', '')
            href = attr_dict.get('href', '')
            if 'text/plain' in t.lower() or href.endswith('.txt') or href.endswith('.txt.utf-8'):
                self.txt_url = href

def sanitize_filename(filename):
    sanitized = re.sub(r'[^\w\s-]', '', filename)
    sanitized = re.sub(r'\s+', ' ', sanitized).strip()
    return sanitized

def download_book(book, data_dir, base_url, target_count, downloaded_count):
    href = book['href']
    if not href.startswith('/ebooks/'):
        return downloaded_count
        
    book_url = urllib.parse.urljoin(base_url, href)
    title = book['title'].replace('\n', ' ').replace('\r', '')
    author = book['author'].replace('\n', ' ').replace('\r', '')
    
    full_title = f"{title} by {author}" if author else title
    safe_title = sanitize_filename(full_title)
    
    file_path = os.path.join(data_dir, f"{safe_title}.txt")
    
    if os.path.exists(file_path):
        print(f"Already exists: {safe_title}")
        return downloaded_count + 1
        
    html = get_html(book_url)
    if not html:
        return downloaded_count
        
    parser = BookPageParser()
    parser.feed(html)
    
    txt_url = parser.txt_url
    if txt_url:
        txt_url = urllib.parse.urljoin(base_url, txt_url)
        # Verify valid scheme to prevent SSRF
        if not txt_url.startswith(('http://', 'https://')):
            print(f"Skipping invalid URL scheme: {txt_url}")
            return downloaded_count
                
        print(f"Downloading [{downloaded_count+1}/{target_count}]: {safe_title}")
        try:
            req = urllib.request.Request(txt_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=20) as resp:
                text = resp.read()
                text = text.decode('utf-8', errors='replace')
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(text)
            time.sleep(1)
            return downloaded_count + 1
        except Exception as e:
            print(f"Error downloading text for {safe_title}: {e}")
    else:
        print(f"No plain text found for: {safe_title}")
        
    return downloaded_count

def main():
    base_url = "https://www.gutenberg.org"
    shelf_url = "https://www.gutenberg.org/ebooks/bookshelf/691"
    
    data_dir = os.path.join(os.getcwd(), 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    downloaded_count = 0
    target_count = 100
    
    current_url = shelf_url
    
    while downloaded_count < target_count and current_url:
        print(f"Fetching shelf page: {current_url}")
        html = get_html(current_url)
        if not html:
            break
            
        parser = LinkParser()
        parser.feed(html)
        
        books = parser.books
        if not books:
            print("No books found. Layout might have changed.")
            break
            
        for book in books:
            if downloaded_count >= target_count:
                break
            downloaded_count = download_book(book, data_dir, base_url, target_count, downloaded_count)
            
        if parser.next_page:
            current_url = urllib.parse.urljoin(base_url, parser.next_page)
            if not current_url.startswith(('http://', 'https://')):
                print(f"Invalid next page URL scheme: {current_url}")
                current_url = None
        else:
            current_url = None
            
    print(f"Finished. Downloaded (or already had) {downloaded_count} books.")

if __name__ == '__main__':
    main()
