import os
import pickle
from config import VECTOR_STORE_PATH, DOCS_PATH, CHUNK_SIZE, SENTENCE_MODEL_NAME, SUPPORTED_DOCS
from sentence_transformers import SentenceTransformer
import faiss
from PyPDF2 import PdfReader
from docx import Document

# ==============================
# HELPER FUNCTIONS TO READ FILES
# ==============================

def read_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def read_pdf(file_path):
    text = ""
    reader = PdfReader(file_path)
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text

def read_docx(file_path):
    doc = Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

def read_all_docs(folder_path):
    """Read all supported documents from the folder"""
    all_texts = []
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        ext = os.path.splitext(file)[1].lower()
        if ext not in SUPPORTED_DOCS:
            continue
        if ext == ".txt":
            all_texts.append(read_txt(file_path))
        elif ext == ".pdf":
            all_texts.append(read_pdf(file_path))
        elif ext == ".docx":
            all_texts.append(read_docx(file_path))
    return all_texts

# ==============================
# CHUNKING FUNCTION
# ==============================
def chunk_text(text, chunk_size=CHUNK_SIZE):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

# ==============================
# BUILD VECTOR STORE
# ==============================
def build_vector_store():
    print("Reading documents from:", DOCS_PATH)
    docs = read_all_docs(DOCS_PATH)
    all_chunks = []
    for doc in docs:
        all_chunks.extend(chunk_text(doc))
    
    if not all_chunks:
        raise ValueError("No documents found in 'docs/' folder or unsupported file types!")

    print(f"Total chunks created: {len(all_chunks)}")

    # Load model
    model = SentenceTransformer(SENTENCE_MODEL_NAME)
    print("Generating embeddings...")
    embeddings = model.encode(all_chunks, convert_to_numpy=True, show_progress_bar=True)

    # Create FAISS index
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    print("FAISS index created with dimension:", dimension)

    # Save chunks
    chunks_file = os.path.join(VECTOR_STORE_PATH, "chunks.pkl")
    with open(chunks_file, "wb") as f:
        pickle.dump(all_chunks, f, protocol=pickle.HIGHEST_PROTOCOL)
    print("Chunks saved to:", chunks_file)

    # Save FAISS index
    faiss_file = os.path.join(VECTOR_STORE_PATH, "faiss_index.bin")
    faiss.write_index(index, faiss_file)
    print("FAISS index saved to:", faiss_file)

    print("Vector store build completed successfully!")

# ==============================
# MAIN EXECUTION
# ==============================
if __name__ == "__main__":
    build_vector_store()
