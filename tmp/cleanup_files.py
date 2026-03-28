import os
import re

def remove_bom(file_path):
    if not os.path.exists(file_path):
        return
    with open(file_path, 'rb') as f:
        content = f.read()
    if content.startswith(b'\xef\xbb\xbf'):
        print(f"Removing BOM from {file_path}")
        with open(file_path, 'wb') as f:
            f.write(content[3:])
    else:
        print(f"No BOM found in {file_path}")

def sanitize_filename(filename):
    # Standard format: philosopher_title.txt (lowercase, underscores)
    # Extract philosopher and title if possible, or just sanitize current
    base = os.path.splitext(filename)[0]
    # Simple sanitization: replace spaces with underscores, lowercase, keep alphanumeric
    # Let's try to match "Title by Author" pattern
    match = re.search(r'(.+)\s+by\s+(.+)', base, re.IGNORECASE)
    if match:
        title, author = match.groups()
        new_name = f"{author}_{title}".lower()
    else:
        new_name = base.lower()
    
    new_name = re.sub(r'[^\w\s-]', '', new_name)
    new_name = re.sub(r'\s+', '_', new_name).strip('_')
    return new_name + ".txt"

def cleanup_data_dir(data_dir):
    for filename in os.listdir(data_dir):
        if not filename.endswith('.txt'):
            continue
        
        file_path = os.path.join(data_dir, filename)
        # 1. Remove BOM
        remove_bom(file_path)
        
        # 2. Rename
        new_filename = sanitize_filename(filename)
        if new_filename != filename:
            new_path = os.path.join(data_dir, new_filename)
            # Check for name collision
            if os.path.exists(new_path):
                 print(f"Collision: {new_filename} already exists. Skipping rename for {filename}")
                 continue
            print(f"Renaming {filename} -> {new_filename}")
            os.rename(file_path, new_path)

if __name__ == "__main__":
    data_dir = r'c:\Users\ysn65\Desktop\antigravity\philo-rag\data'
    readme_path = r'c:\Users\ysn65\Desktop\antigravity\philo-rag\README.md'
    
    print("Cleaning up data files...")
    cleanup_data_dir(data_dir)
    
    print("\nRemoving BOM from README.md...")
    remove_bom(readme_path)
    print("\nDone.")
