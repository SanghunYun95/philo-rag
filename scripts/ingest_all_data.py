import os
import sys

# Force UTF-8 encoding for standard output to prevent cp949 encoding errors on Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
# Ensure we can import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.ingest_data import ingest_document

def main():
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
    if not os.path.exists(data_dir):
        print(f"Data directory not found at {data_dir}")
        return

    failed_files = []
    
    files = [f for f in os.listdir(data_dir) if f.endswith(".txt")]
    print(f"Found {len(files)} text files in {data_dir}.")
    
    for idx, filename in enumerate(files):
        filepath = os.path.join(data_dir, filename)
        
        # Parse filename backwards to find the last " by "
        name_without_ext = filename[:-4]
        parts = name_without_ext.rsplit(" by ", 1)
        
        if len(parts) == 2:
            title = parts[0].strip()
            philosopher = parts[1].strip()
        else:
            title = name_without_ext
            philosopher = "Unknown"
            
        school = "Philosophy" # We'll just use a generic school for now
        
        print(f"\n[{idx+1}/{len(files)}] ==================================")
        print(f"Processing: {title} by {philosopher}")
        print(f"==================================================")
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                text = f.read()
                
            # Skipping if text is too short
            if len(text) < 1000:
                print(f"Skipping {filename}: Text too short ({len(text)} chars).")
                continue
                
            ingest_document(text, philosopher, school, title)
            
        except Exception as e:
            print(f"Failed to process {filename}: {e}")
            failed_files.append(filename)

    if failed_files:
        print("\nFailed processing for the following files:")
        for f in failed_files:
            print(f)
    else:
        print("\nAll files processed successfully!")

if __name__ == "__main__":
    main()
