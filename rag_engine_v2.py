
import json
import os
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Model multilingual → lebih baik untuk 🇩🇪/🇬🇧
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

DATA_DIR = "data/faiss_index"
INDEX_PATH = os.path.join(DATA_DIR, "planville.index")
DOCS_PATH = os.path.join(DATA_DIR, "docs.json")

# Global cache
cached_index = None
cached_docs = None

def load_index_and_docs():
    global cached_index, cached_docs
    if cached_index is None or cached_docs is None:
        with open(DOCS_PATH, encoding="utf-8") as f:
            cached_docs = json.load(f)
        cached_index = faiss.read_index(INDEX_PATH)
    return cached_index, cached_docs

def build_vector_store():
    with open("data/docs.json", encoding="utf-8") as f:
        docs_raw = json.load(f)
    texts = [d["text"] for d in docs_raw]
    embeddings = model.encode(texts, show_progress_bar=True)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(np.array(embeddings))

    os.makedirs(DATA_DIR, exist_ok=True)
    faiss.write_index(index, INDEX_PATH)
    with open(DOCS_PATH, "w", encoding="utf-8") as f:
        json.dump(docs_raw, f, ensure_ascii=False)

def query_index(query, top_k=3, min_score=0.5):
    index, docs = load_index_and_docs()
    q_emb = model.encode([query])
    D, I = index.search(np.array(q_emb), top_k)

    results = []
    for idx, score in zip(I[0], D[0]):
        if idx < len(docs):
            relevance = float(np.exp(-score))  # Skor jarak → relevansi
            if relevance >= min_score:
                doc = docs[idx]
                results.append({
                    "text": doc.get("text", ""),
                    "source": doc.get("source", ""),
                    "scraped_at": doc.get("scraped_at", ""),
                    "score": round(relevance, 4)
                })
    return results

if __name__ == "__main__":
    build_vector_store()
