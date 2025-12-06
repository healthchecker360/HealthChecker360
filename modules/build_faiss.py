import os
import pickle
import faiss
from sentence_transformers import SentenceTransformer
from pathlib import Path
from PyPDF2 import PdfReader
import docx

# ------------------------------
# PATHS
# ------------------------------
DOCS_PATH = Path("docs")
VECTOR_PATH = Path("vector_store")
VECTOR_PATH.mkdir(exist_ok=True)

CHUNKS_FILE = VECTOR_PATH / "chunks.pkl"
INDEX_FILE = VECTOR_PATH / "faiss_index.bin"

# ------------------------------
# LOAD DOCS
# ------------------------------
def load_documents():
    documents = []
    for file in DOCS_PATH.iterdir():
        if file.suffix.lower() == ".pdf":
            reader = PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
            documents.append(text)
        elif file.suffix.lower() == ".txt":
            with open(file, "r", encoding="utf-8") as f:
                documents.append(f.read())
        elif file.suffix.lower() == ".docx":
            doc = docx.Document(file)
            text = "\n".join([para.text for para in doc.paragraphs])
            documents.append(text)
    return documents

# ------------------------------
# SPLIT INTO CHUNKS
# ------------------------------
def split_text(text, chunk_size=500, overlap=50):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks

# ------------------------------
# BUILD FAISS INDEX
# ------------------------------
def build_faiss_index():
    print("Loading documents...")
    documents = load_documents()
    all_chunks = []

    for doc in documents:
        chunks = split_text(doc)
        all_chunks.extend(chunks)

    print(f"Total chunks: {len(all_chunks)}")

    # Create embeddings
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(all_chunks, show_progress_bar=True)
    embeddings = embeddings.astype("float32")

    # Build FAISS index
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    # Save
    with open(CHUNKS_FILE, "wb") as f:
        pickle.dump(all_chunks, f)
    faiss.write_index(index, str(INDEX_FILE))
    print("FAISS index and chunks saved successfully.")

# ------------------------------
# RUN
# ------------------------------
if __name__ == "__main__":
    build_faiss_index()
