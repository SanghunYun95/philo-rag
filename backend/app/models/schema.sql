-- Enable the pgvector extension to work with embedding vectors
create extension if not exists vector;

-- Create a table to store your documents
CREATE TABLE documents (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  content text NOT NULL, -- English text chunk
  embedding vector(1536), -- Vector data (1536 dims for text-embedding-ada-002, huggingface dims may vary, adjust if using a different local model e.g. 384 for sentence-transformers all-MiniLM-L6-v2)
  metadata jsonb NOT NULL -- Metadata including philosopher, school of thought, and book info
);

-- Note: If you use a local model like `all-MiniLM-L6-v2`, the dimension will be 384. 
-- The user prompt mentioned "1536-dimensional vectors" (which is typical for OpenAI), but also mentioned "local HuggingFace model". 
-- We'll assume the user indeed wants 1536, perhaps they have a specific local model in mind (e.g., modern BERT variants or they intend to match OpenAI dimensions). 

-- Create a function to search for documents
create or replace function match_documents (
  query_embedding vector(1536),
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
