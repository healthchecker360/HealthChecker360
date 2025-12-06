import os
import pickle
import faiss
from sentence_transformers import SentenceTransformer
from PyPDF2 import PdfReader
from docx import Document

VECTOR_FOLDER = os.path.join(os.path.dirname(__file__), "vector_store")
DOCS_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), "docs")
CHUNK_SIZE = 500
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# Create vector folder if not exists
os.makedirs(VECTOR_FOLDER, exist_ok=True)

def read_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def read_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def read_docx(file_path):
    doc = Document(file_path)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

def read_all_docs(folder_path):
    docs = []
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        if file.endswith(".txt"):
            docs.append(read_txt(file_path))
        elif file.endswith(".pdf"):
            docs.append(read_pdf(file_path))
        elif file.endswith(".docx"):
            docs.append(read_docx(file_path))
    return docs

def chunk_text(text, chunk_size=CHUNK_SIZE):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end
    return chunks

def build_vector_store():
    docs = read_all_docs(DOCS_FOLDER)
    all_chunks = []
    for doc in docs:
        all_chunks.extend(chunk_text(doc))

    print(f"Total chunks: {len(all_chunks)}")

    model = SentenceTransformer(MODEL_NAME)
    embeddings = model.encode(all_chunks, show_progress_bar=True, convert_to_numpy=True)

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    # Save chunks
    chunks_path = os.path.join(VECTOR_FOLDER, "chunks.pkl")
    with open(chunks_path, "wb") as f:
        pickle.dump(all_chunks, f, protocol=pickle.HIGHEST_PROTOCOL)

    # Save FAISS index
    index_path = os.path.join(VECTOR_FOLDER, "faiss_index.bin")
    faiss.write_index(index, index_path)

    print("Vector store built successfully!")

if __name__ == "__main__":
    build_vector_store()
