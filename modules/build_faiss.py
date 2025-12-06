import os
import pickle
from sentence_transformers import SentenceTransformer
import faiss

# Paths
VECTOR_FOLDER = os.path.join(os.path.dirname(__file__), "vector_store")
DOCS_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), "docs")

# Chunk size
CHUNK_SIZE = 500

# Model
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# Create vector folder if not exists
os.makedirs(VECTOR_FOLDER, exist_ok=True)

def read_txt_files(folder_path):
    docs = []
    for file in os.listdir(folder_path):
        if file.endswith(".txt"):
            with open(os.path.join(folder_path, file), "r", encoding="utf-8") as f:
                docs.append(f.read())
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
    docs = read_txt_files(DOCS_FOLDER)
    all_chunks = []
    for doc in docs:
        all_chunks.extend(chunk_text(doc))

    print(f"Total chunks: {len(all_chunks)}")

    model = SentenceTransformer(MODEL_NAME)
    embeddings = model.encode(all_chunks, show_progress_bar=True, convert_to_numpy=True)

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    # Save chunks with latest protocol
    chunks_path = os.path.join(VECTOR_FOLDER, "chunks.pkl")
    with open(chunks_path, "wb") as f:
        pickle.dump(all_chunks, f, protocol=pickle.HIGHEST_PROTOCOL)

    # Save FAISS index
    index_path = os.path.join(VECTOR_FOLDER, "faiss_index.bin")
    faiss.write_index(index, index_path)

    print("Vector store built successfully!")

if __name__ == "__main__":
    build_vector_store()
