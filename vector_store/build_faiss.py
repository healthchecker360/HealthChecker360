# build_faiss.py
import os
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle

PDF_FOLDER = "pdfs"
VECTOR_FOLDER = "vector_store"
MODEL_NAME = "all-MiniLM-L6-v2"  # SentenceTransformer model

# Load embedding model
model = SentenceTransformer(MODEL_NAME)

# Read all PDFs
texts = []
for file in os.listdir(PDF_FOLDER):
    if file.endswith(".pdf"):
        reader = PdfReader(os.path.join(PDF_FOLDER, file))
        for page in reader.pages:
            text = page.extract_text()
            if text:
                texts.append(text)

# Create embeddings
embeddings = model.encode(texts, convert_to_numpy=True)

# Build FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

# Save FAISS index
if not os.path.exists(VECTOR_FOLDER):
    os.makedirs(VECTOR_FOLDER)

faiss.write_index(index, os.path.join(VECTOR_FOLDER, "faiss_index.idx"))

# Save texts for retrieval mapping
with open(os.path.join(VECTOR_FOLDER, "texts.pkl"), "wb") as f:
    pickle.dump(texts, f)

print("✅ FAISS vector store built successfully!")
