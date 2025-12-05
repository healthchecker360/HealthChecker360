import os
import faiss
import pickle
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer
from config import PDF_FOLDER, VECTOR_STORE_PATH, TOP_K

# Initialize embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')


# ------------------------------
# PDF Text Extraction & Chunking
# ------------------------------
def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + " "
    return text

def chunk_text(text, chunk_size=500, overlap=50):
    """
    Split text into overlapping chunks for better retrieval.
    chunk_size: number of words per chunk
    overlap: number of overlapping words
    """
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i+chunk_size])
        chunks.append(chunk)
    return chunks


# ------------------------------
# Build FAISS Index from PDFs
# ------------------------------
def build_faiss_index():
    all_chunks = []
    pdf_files = [f for f in os.listdir(PDF_FOLDER) if f.endswith(".pdf")]

    print(f"[INFO] Found {len(pdf_files)} PDFs. Processing...")

    for pdf in pdf_files:
        pdf_path = os.path.join(PDF_FOLDER, pdf)
        text = extract_text_from_pdf(pdf_path)
        chunks = chunk_text(text)
        all_chunks.extend(chunks)

    print(f"[INFO] Total chunks created: {len(all_chunks)}")

    # Create embeddings
    embeddings = model.encode(all_chunks, show_progress_bar=True)

    # Create FAISS index
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    # Save index and chunks
    if not os.path.exists(os.path.dirname(VECTOR_STORE_PATH)):
        os.makedirs(os.path.dirname(VECTOR_STORE_PATH))

    faiss.write_index(index, VECTOR_STORE_PATH + ".index")
    with open(VECTOR_STORE_PATH + "_chunks.pkl", "wb") as f:
        pickle.dump(all_chunks, f)

    print(f"[INFO] FAISS index and chunks saved at {VECTOR_STORE_PATH}")


# ------------------------------
# RAG Retrieval
# ------------------------------
def retrieve_relevant_chunks(query, top_k=TOP_K):
    """
    Given a user query, return top-k most relevant PDF chunks.
    """
    # Load FAISS index and chunks if not already loaded
    global index, all_chunks
    if 'index' not in globals() or 'all_chunks' not in globals():
        index = faiss.read_index(VECTOR_STORE_PATH + ".index")
        with open(VECTOR_STORE_PATH + "_chunks.pkl", "rb") as f:
            all_chunks = pickle.load(f)

    # Convert query to embedding
    query_embedding = model.encode([query])

    # Search FAISS index
    distances, indices = index.search(query_embedding, top_k)

    # Retrieve corresponding chunks
    results = [all_chunks[i] for i in indices[0]]
    return results


# ------------------------------
# Run as script
# ------------------------------
if __name__ == "__main__":
    build_faiss_index()
