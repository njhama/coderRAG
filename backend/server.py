from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import faiss
import json
import numpy as np
from sentence_transformers import SentenceTransformer
import os

# Initialize FastAPI app
app = FastAPI()

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend URL
    allow_credentials=True,                  # If cookies or tokens are sent
    allow_methods=["*"],                     # Allow all HTTP methods
    allow_headers=["*"],                     # Allow all custom headers
)

# Define paths to the data directory and files
base_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(base_dir, "../data")
faiss_index_path = os.path.join(data_dir, "faiss_index")
json_data_path = os.path.join(data_dir, "final.json")

# Load FAISS index and dataset
index = faiss.read_index(faiss_index_path)
with open(json_data_path, 'r') as f:
    data = json.load(f)

# Initialize embedding model
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# Define the request body model
class QueryRequest(BaseModel):
    query: str
    k: int = 3  # Number of results to return

# Define the API endpoint to retrieve results
@app.post("/retrieve")
def retrieve(query_request: QueryRequest):
    """
    Retrieve top-k similar questions based on the query.
    """
    query_embedding = embedding_model.encode([query_request.query])
    _, indices = index.search(np.array(query_embedding), query_request.k)
    results = [
        {
            "question": data[i]["question_description"],
            "solution_code": data[i]["solution_code"]
        }
        for i in indices[0]
    ]
    return {"results": results}

# Define a success endpoint
@app.get("/success")
def success():
    """
    Health check or success endpoint.
    """
    return {"status": "success", "message": "The server is running properly!"}
