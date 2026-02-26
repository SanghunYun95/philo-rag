import sys
from app.services.database import supabase_client

try:
    # Try to select from documents to check if the table exists
    res = supabase_client.table('documents').select('id').limit(1).execute()
    print('Table exists')
    if res.data:
        print('Found at least 1 row')
    else:
        print('Table is empty')
except Exception as e:
    error_msg = str(e).lower()
    if (
        'relation "documents" does not exist' in error_msg
        or 'table missing' in error_msg
        or '42p01' in error_msg
    ):
        print("Table 'documents' does not exist yet. Please run migrations.")
        sys.exit(1)
    else:
        print(f"Database connection or query error: {e}")
        raise
