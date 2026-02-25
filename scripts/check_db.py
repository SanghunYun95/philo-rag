import sys
from app.services.database import supabase_client

try:
    # Try to select from documents to check if the table exists
    res = supabase_client.table('documents').select('id').limit(1).execute()
    print('Table exists')
    if res.data:
        print(f'Found {len(res.data)} rows')
    else:
        print('Table is empty')
except Exception as e:
    print(f'Error or Table does not exist: {e}')
    # No exit(1) because we want to know if it's just not there
