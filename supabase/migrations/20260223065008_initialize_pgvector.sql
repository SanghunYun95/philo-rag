-- Enable the pgvector extension to work with embedding vectors
create extension if not exists vector;

-- Create a table to store your documents
CREATE TABLE documents (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  content text NOT NULL, -- English text chunk
  embedding vector(3072), -- Vector data (3072 dims for gemini-embedding-001)
  metadata jsonb NOT NULL -- Metadata including philosopher, school of thought, and book info
);

-- Note: We are using `gemini-embedding-001` which has 3072 dimensions.

-- Create a function to search for documents
create or replace function match_documents (
  query_embedding vector(3072),
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
