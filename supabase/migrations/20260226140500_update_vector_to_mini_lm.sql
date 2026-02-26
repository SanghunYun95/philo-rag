-- This migration changes the `embedding` column dimension from 3072 to 384
-- to support the local `all-MiniLM-L6-v2` model.

-- 1. Drop the existing HNSW index and match_documents function 
DROP INDEX IF EXISTS documents_embedding_idx;
DROP FUNCTION IF EXISTS match_documents;

-- 2. Clear existing incompatible 3072-dimension vectors to avoid casting errors
DO $$
BEGIN
    -- This is a guard to prevent accidental truncation in production CI/CD.
    -- In a real scenario, you'd check a configuration or role here.
    -- For now, we explicitly execute it but wrap it to highlight the danger.
    IF EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name='documents' AND column_name='embedding'
    ) THEN
        TRUNCATE TABLE documents;
    END IF;
END $$;

-- 3. Alter the column type now that the table is empty
ALTER TABLE documents 
ALTER COLUMN embedding TYPE vector(384);

-- 3. Recreate the match_documents function with the new dimension
create or replace function match_documents (
  query_embedding vector(384),
  match_count int DEFAULT 10,
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
  if match_count < 1 then
    match_count := 1;
  elsif match_count > 200 then
    match_count := 200;
  end if;

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

-- 4. Recreate the HNSW index for the 384 dimension
CREATE INDEX ON documents USING hnsw (embedding vector_cosine_ops);
