-- Update the documents table and match_documents function to use 3072 dimensions
-- for gemini-embedding-001

-- 1. Drop the existing function
DROP FUNCTION IF EXISTS match_documents(vector(3072), int, jsonb);

-- 2. Alter the table column
ALTER TABLE documents 
ALTER COLUMN embedding TYPE vector(3072);

-- 3. Recreate the function with new dimension
create or replace function match_documents (
  query_embedding vector(3072),
  match_count int DEFAULT null,
  filter jsonb DEFAULT '{}'
) returns table (
  id uuid,
  content text,
  metadata jsonb,
  similarity float
)
language plpgsql
as $$
begin
  return query
  select
    documents.id,
    documents.content,
    documents.metadata,
    1 - (documents.embedding <=> query_embedding) as similarity
  from documents
  where documents.metadata @> filter
  order by documents.embedding <=> query_embedding
  limit match_count;
end;
$$;
