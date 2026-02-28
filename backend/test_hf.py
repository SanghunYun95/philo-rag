import sys
sys.path.append(r"c:\Users\ysn65\Desktop\antigravity\philo-rag\backend")
from langchain_community.embeddings import HuggingFaceEmbeddings

def test():
    print("Loading HuggingFaceEmbeddings...")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vec = embeddings.embed_query("Hello")
    print(f"Dimension: {len(vec)}")

if __name__ == "__main__":
    test()
