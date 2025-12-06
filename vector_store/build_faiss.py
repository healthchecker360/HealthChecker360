import os
import pickle
from sentence_transformers import SentenceTransformer
import faiss

# ------------------------------
# CONFIG
# ------------------------------
VECTOR_FOLDER = "vector_store"
DOCS_FOLDER = "docs"  # Put your .txt documents here
CHUNK_SIZE = 500       # Characters per chunk
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

os.makedirs(VECTOR_FOLDER, exist_ok=True)

# ------------------------------
# Read .txt files
# ------------------------------
def read_txt_files(folder_path):
    docs = []
    for file in os.listdir(folder_path):
        if file.endswith(".txt"):
            with open(os.path.join(folder_path, file), "r", encoding="utf-8") as f:
                docs.append(f.read())
    return docs

# ------------------------------
# Split text into chunks
# ------------------------------
def chunk_text(text, chunk_size=CHUNK_SIZE):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end
    return chunks

# ------------------------------
# Build FAISS index
# ------------------------------
def build_vector_store():
    print("Reading documents...")
    docs = read_txt_files(DOCS_FOLDER)
    all_chunks = []
    for doc in docs:
        all_chunks.extend(chunk_text(doc))

    print(f"Total chunks: {len(all_chunks)}")

    print("Generating embeddings...")
    model = SentenceTransformer(MODEL_NAME)
    embeddings = model.encode(all_chunks, show_progress_bar=True, convert_to_numpy=True)

    print("Building FAISS index...")
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    # Save chunks and index
    with open(os.path.join(VECTOR_FOLDER, "chunks.pkl"), "wb") as f:
        pickle.dump(all_chunks, f)

    faiss.write_index(index, os.path.join(VECTOR_FOLDER, "faiss_index.bin"))

    print("Vector store built successfully!")

# ------------------------------
# Run script
# ------------------------------
if __name__ == "__main__":
    build_vector_store()
