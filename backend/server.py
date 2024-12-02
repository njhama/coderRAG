from fastapi import FastAPI
from pydantic import BaseModel
import faiss
import json
import numpy as np
from sentence_transformers import SentenceTransformer

app = FastAPI()

index = faiss.read_index('data/faiss_index')
with open('data/final.json', 'r') as f:
    data = json.load(f)

embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

class QueryRequest(BaseModel):
    query: str
    k: int = 3  

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
