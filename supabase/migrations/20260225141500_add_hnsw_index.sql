-- Add HNSW index to the documents table to optimize vector search performance
-- Since the vector dimension is 3072 (exceeds the 2000 limit for vector hnsw index),
-- we cast the embedding to halfvec(3072) for indexing.
CREATE INDEX IF NOT EXISTS documents_embedding_idx ON documents USING hnsw ((embedding::halfvec(3072)) halfvec_cosine_ops);

-- Update the match_documents function to ensure the index is used by casting the query
CREATE OR REPLACE FUNCTION match_documents (
  query_embedding vector(3072),
  match_count int DEFAULT null,
  filter jsonb DEFAULT '{}'
) RETURNS TABLE (
  id uuid,
  content text,
  metadata jsonb,
  similarity float
)
LANGUAGE plpgsql
AS $$
BEGIN
  RETURN QUERY
  SELECT
    documents.id,
    documents.content,
    documents.metadata,
    1 - ((documents.embedding::halfvec(3072)) <=> (query_embedding::halfvec(3072))) AS similarity
  FROM documents
  WHERE documents.metadata @> filter
  ORDER BY (documents.embedding::halfvec(3072)) <=> (query_embedding::halfvec(3072))
  LIMIT match_count;
END;
$$;
