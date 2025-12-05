import os
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle

# ------------------------------
# Folders
# ------------------------------
PDF_FOLDER = "pdfs"          # PDFs for ingestion
VECTOR_FOLDER = "vector_store"  # FAISS index storage

# ------------------------------
# Load embedding model
# ------------------------------
MODEL_NAME = "all-MiniLM-L6-v2"  # You can change to any sentence-transformers model
model = SentenceTransformer(MODEL_NAME)

# ------------------------------
# Read and extract text from PDFs
# ------------------------------
texts = []

for file in os.listdir(PDF_FOLDER):
    if file.endswith(".pdf"):
        pdf_path = os.path.join(PDF_FOLDER, file)
        reader = PdfReader(pdf_path)
        for page in reader.pages:
            text = page.extract_text()
            if text:
                texts.append(text)

if len(texts) == 0:
    print("⚠️ No text found in PDFs. Please check your pdfs/ folder.")
    exit()

# ------------------------------
# Generate embeddings
# ------------------------------
print("🔹 Generating embeddings...")
embeddings = model.encode(texts, convert_to_numpy=True)

# ------------------------------
# Build FAISS index
# ------------------------------
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

# ------------------------------
# Save FAISS index and text mapping
# ------------------------------
if not os.path.exists(VECTOR_FOLDER):
    os.makedirs(VECTOR_FOLDER)

faiss.write_index(index, os.path.join(VECTOR_FOLDER, "faiss_index.idx"))

with open(os.path.join(VECTOR_FOLDER, "texts.pkl"), "wb") as f:
    pickle.dump(texts, f)

print(f"✅ FAISS vector store built successfully!")
print(f"Index saved at: {VECTOR_FOLDER}/faiss_index.idx")
print(f"Texts mapping saved at: {VECTOR_FOLDER}/texts.pkl")
