# rag_engine.py
import os
import json
import faiss
import numpy as np
import pdfplumber
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
VECTOR_STORE_PATH = os.getenv("VECTOR_STORE_PATH", "vector_store/")

# Ensure vector store folder exists
if not os.path.exists(VECTOR_STORE_PATH):
    os.makedirs(VECTOR_STORE_PATH)

# -------------------------
# Sentence Transformer Model
# -------------------------
# We use a lightweight model suitable for CPU
MODEL_NAME = "all-MiniLM-L6-v2"
embedder = SentenceTransformer(MODEL_NAME)

# -------------------------
# Index Helpers
# -------------------------
INDEX_FILE = os.path.join(VECTOR_STORE_PATH, "faiss_index.bin")
METADATA_FILE = os.path.join(VECTOR_STORE_PATH, "metadata.json")

# Metadata format: list of dicts with {"text": "...", "source": "filename.pdf"}
metadata = []

# -------------------------
# Load or create FAISS index
# -------------------------
def load_index():
    global index, metadata
    if os.path.exists(INDEX_FILE) and os.path.exists(METADATA_FILE):
        index = faiss.read_index(INDEX_FILE)
        with open(METADATA_FILE, "r", encoding="utf-8") as f:
            metadata = json.load(f)
        print(f"[RAG] Loaded existing FAISS index with {index.ntotal} entries.")
    else:
        index = faiss.IndexFlatL2(embedder.get_sentence_embedding_dimension())
        print("[RAG] Created new empty FAISS index.")

# -------------------------
# Ingest PDF and create embeddings
# -------------------------
def ingest_pdf(pdf_path):
    global index, metadata
    if not os.path.exists(pdf_path):
        print(f"[RAG] File not found: {pdf_path}")
        return

    print(f"[RAG] Processing {pdf_path}...")
    chunks = []

    # Extract text from PDF
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                # Simple chunking: split by 500 characters
                for i in range(0, len(text), 500):
                    chunk = text[i:i+500].strip()
                    if chunk:
                        chunks.append(chunk)

    # Embed chunks
    embeddings = embedder.encode(chunks, convert_to_numpy=True)

    # Add to FAISS index
    if not hasattr(index, "ntotal"):
        load_index()
    index.add(embeddings)

    # Add metadata
    for chunk in chunks:
        metadata.append({"text": chunk, "source": os.path.basename(pdf_path)})

    # Save index and metadata
    faiss.write_index(index, INDEX_FILE)
    with open(METADATA_FILE, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)

    print(f"[RAG] Ingested {len(chunks)} chunks from {pdf_path}.")

# -------------------------
# Query RAG
# -------------------------
def query_rag(query, top_k=3):
    if not hasattr(index, "ntotal") or index.ntotal == 0:
        print("[RAG] No index found. Please ingest PDFs first.")
        return []

    query_embedding = embedder.encode([query], convert_to_numpy=True)
    distances, indices = index.search(query_embedding, top_k)

    results = []
    for idx in indices[0]:
        if idx < len(metadata):
            results.append(metadata[idx])
    return results

# -------------------------
# Initialize
# -------------------------
load_index()
