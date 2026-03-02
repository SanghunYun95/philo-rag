import json
import os

def generate_sql():
    # Load mapping
    mapping_path = os.path.join("data", "books_mapping.json")
    with open(mapping_path, "r", encoding="utf-8") as f:
        mapping_data = json.load(f)

    # 1. Create a B-Tree index on the title field to make string matching instant
    # instead of doing a full sequential table scan
    sql_statements = [
        "CREATE INDEX IF NOT EXISTS idx_documents_book_title ON documents ((metadata->'book_info'->>'title'));\n",
        "SET statement_timeout = '120s'; -- Increase timeout to be safe\n"
    ]
    
    for book in mapping_data:
        original_file = book.get("original_file", "")
        name_without_ext = original_file[:-4]
        parts = name_without_ext.rsplit(" by ", 1)
        if len(parts) == 2:
            title = parts[0].strip()
        else:
            title = name_without_ext
            
        title_to_match = f"Korean Translation of {title}"
        
        kr_title = book.get("translated_title", "")
        aladin = book.get("aladin_data", {})
        thumbnail = aladin.get("thumbnail", "")
        link = aladin.get("link", "")
        
        # Escape single quotes in strings for SQL
        kr_title_esc = kr_title.replace("'", "''")
        thumbnail_esc = thumbnail.replace("'", "''")
        link_esc = link.replace("'", "''")
        title_to_match_esc = title_to_match.replace("'", "''")
        
        jsonb_payload = json.dumps({
            "kr_title": kr_title,
            "thumbnail": thumbnail,
            "link": link
        }, ensure_ascii=False)
        
        # Double the single quotes inside the json string for the SQL literal
        jsonb_payload_esc = jsonb_payload.replace("'", "''")
        
        sql = f"""UPDATE documents
SET metadata = metadata || '{jsonb_payload_esc}'::jsonb
WHERE metadata->'book_info'->>'title' = '{title_to_match_esc}';"""
        
        sql_statements.append(sql)

    output_path = "update_metadata.sql"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n\n".join(sql_statements))
        
    print(f"Generated {output_path} with {len(sql_statements)} UPDATE statements.")

if __name__ == "__main__":
    generate_sql()
