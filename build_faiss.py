import os
import pickle
import faiss
from sentence_transformers import SentenceTransformer

from config import VECTOR_FOLDER, FAISS_INDEX_PATH, CHUNKS_PATH, EMBED_MODEL


# -----------------------------------------------------
# Load text files & prepare raw data
# -----------------------------------------------------
def load_text_files(folder_path="data"):
    """
    Loads all .txt files in the 'data' folder.
    Every file's content becomes part of the knowledge base.
    """
    documents = []

    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"'data' folder not found: {folder_path}")

    for filename in os.listdir(folder_path):
        if filename.endswith(".txt") or filename.endswith(".md"):
            full_path = os.path.join(folder_path, filename)
            with open(full_path, "r", encoding="utf-8") as f:
                documents.append(f.read())

    if len(documents) == 0:
        raise ValueError("No text files found in 'data' folder.")

    return documents


# -----------------------------------------------------
# Split text into chunks
# -----------------------------------------------------
def chunk_text(text, chunk_size=400):
    """
    Splits long text into smaller chunks for embedding.
    """
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)

    return chunks


# -----------------------------------------------------
# Build FAISS Index
# -----------------------------------------------------
def build_faiss_index():
    print("🔄 Loading documents...")
    documents = load_text_files()

    print("🔄 Splitting into chunks...")
    all_chunks = []
    for doc in documents:
        all_chunks.extend(chunk_text(doc))

    print(f"📦 Total chunks created: {len(all_chunks)}")

    # Load SentenceTransformer
    print("🔄 Loading embedding model...")
    embedder = SentenceTransformer(EMBED_MODEL)

    # Create vectors
    print("🔄 Creating embeddings...")
    embeddings = embedder.encode(all_chunks, show_progress_bar=True)

    # Convert to float32 for FAISS
    embeddings = embeddings.astype("float32")

    # Create FAISS index
    print("🔄 Building FAISS index...")
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)

    index.add(embeddings)

    # Ensure vector_store exists
    os.makedirs(VECTOR_FOLDER, exist_ok=True)

    # Save FAISS index
    print("💾 Saving FAISS index...")
    faiss.write_index(index, FAISS_INDEX_PATH)

    # Save chunks
    print("💾 Saving chunks...")
    with open(CHUNKS_PATH, "wb") as f:
        pickle.dump(all_chunks, f)

    print("\n✅ FAISS index built successfully!")
    print(f"📁 Saved to: {FAISS_INDEX_PATH}")
    print(f"📁 Saved to: {CHUNKS_PATH}")


if __name__ == "__main__":
    build_faiss_index()
