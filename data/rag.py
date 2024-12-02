import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load your dataset
with open('final.json', 'r') as f:
    data = json.load(f)

# Extract question descriptions for embeddings
descriptions = [entry['question_description'] for entry in data]

# Generate embeddings using SentenceTransformers
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = embedding_model.encode(descriptions)

# Create a FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)  # L2 distance
index.add(np.array(embeddings))

# Save the index for future use
faiss.write_index(index, 'faiss_index')
