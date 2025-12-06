import os
import pickle
from pathlib import Path

import faiss
from sentence_transformers import SentenceTransformer
from PyPDF2 import PdfReader
import docx

from config import DOCS_PATH, VECTOR_PATH, FAISS_INDEX_PATH, CHUNKS_FILE_PATH, CHUNK_SIZE, CHUNK_OVERLAP, DEBUG

# ------------------------------
# Load documents from pdf, txt, docx
# ------------------------------
def load_documents():
    documents = []
    for file in DOCS_PATH.iterdir():
        try:
            if file.suffix.lower() == ".pdf":
                reader = PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() or ""
                if text.strip():
                    documents.append(text)
            elif file.suffix.lower() == ".txt":
                with open(file, "r", encoding="utf-8") as f:
                    text = f.read()
                    if text.strip():
                        documents.append(text)
            elif file.suffix.lower() == ".docx":
                doc = docx.Document(file)
                text = "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
                if text.strip():
                    documents.append(text)
        except Exception as e:
            if DEBUG:
                print(f"Error reading {file.name}: {e}")
    if DEBUG:
        print(f"Loaded {len(documents)} documents from {DOCS_PATH}")
    return documents

# ------------------------------
# Split text into chunks
# ------------------------------
def split_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks

# ------------------------------
# Build FAISS index
# ------------------------------
def build_faiss_index():
    documents = load_documents()
    all_chunks = []
    for doc in documents:
        all_chunks.extend(split_text(doc))
    
    if not all_chunks:
        print("No documents found to build FAISS index.")
        return

    # Embeddings
    print("Generating embeddings...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(all_chunks, show_progress_bar=True)
    embeddings = embeddings.astype("float32")

    # Build FAISS index
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    # Save index and chunks
    faiss.write_index(index, str(FAISS_INDEX_PATH))
    with open(CHUNKS_FILE_PATH, "wb") as f:
        pickle.dump(all_chunks, f)
    
    print(f"FAISS index and chunks saved successfully! Total chunks: {len(all_chunks)}")

# ------------------------------
# Run
# ------------------------------
if __name__ == "__main__":
    build_faiss_index()
