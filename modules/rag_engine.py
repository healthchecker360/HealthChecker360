import os
import pickle
from pathlib import Path
import faiss
from sentence_transformers import SentenceTransformer
from modules.config import DOCS_FOLDER, VECTOR_FOLDER, CHUNKS_FILE, FAISS_INDEX_FILE, TOP_K_CHUNKS

# ------------------------------
# Load / Build FAISS Index
# ------------------------------
def build_vector_store():
    """
    Reads all docs (PDF, TXT, DOCX), creates chunks, embeddings, and saves FAISS index.
    """
    VECTOR_FOLDER.mkdir(exist_ok=True)

    # Initialize model
    model = SentenceTransformer('all-MiniLM-L6-v2')

    chunks = []
    embeddings = []

    # Iterate through docs folder
    for file_path in DOCS_FOLDER.glob("*"):
        ext = file_path.suffix.lower()
        text = ""
        try:
            if ext == ".txt":
                text = file_path.read_text(encoding="utf-8")
            elif ext == ".pdf":
                from PyPDF2 import PdfReader
                reader = PdfReader(str(file_path))
                text = "\n".join([page.extract_text() or "" for page in reader.pages])
            elif ext == ".docx":
                import docx
                doc = docx.Document(str(file_path))
                text = "\n".join([para.text for para in doc.paragraphs])
        except Exception as e:
            print(f"Error reading {file_path.name}: {e}")
            continue

        # Split into chunks
        text_chunks = split_text_into_chunks(text)
        chunks.extend(text_chunks)
        embeddings.extend(model.encode(text_chunks))

    if not chunks:
        raise ValueError("No text chunks found in docs folder!")

    # Build FAISS index
    dim = len(embeddings[0])
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings).astype('float32'))

    # Save index and chunks
    faiss.write_index(index, str(FAISS_INDEX_FILE))
    with open(CHUNKS_FILE, "wb") as f:
        pickle.dump(chunks, f)

    return index, chunks

# ------------------------------
# Split text into chunks
# ------------------------------
def split_text_into_chunks(text, chunk_size=500):
    """
    Splits large text into smaller chunks for vectorization
    """
    text = text.replace("\n", " ").strip()
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunks.append(" ".join(words[i:i + chunk_size]))
    return chunks

# ------------------------------
# Load FAISS index
# ------------------------------
def load_vector_store():
    """
    Loads FAISS index and chunks; if missing, instructs to build
    """
    if FAISS_INDEX_FILE.exists() and CHUNKS_FILE.exists():
        index = faiss.read_index(str(FAISS_INDEX_FILE))
        with open(CHUNKS_FILE, "rb") as f:
            chunks = pickle.load(f)
        return index, chunks
    else:
        raise FileNotFoundError("FAISS index or chunks file not found! Run build_faiss.py first.")

# ------------------------------
# Retrieve top-k relevant chunks
# ------------------------------
def retrieve_relevant_chunks(query, top_k=TOP_K_CHUNKS):
    """
    Returns top-k chunks relevant to the query
    """
    index, chunks = load_vector_store()
    model = SentenceTransformer('all-MiniLM-L6-v2')
    query_vec = model.encode([query])
    D, I = index.search(query_vec.astype('float32'), top_k)
    results = [chunks[i] for i in I[0] if i < len(chunks)]
    return results
