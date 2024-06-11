from fastapi import FastAPI
from pydantic import BaseModel

from mistral_client import MistralClient
from retrieval_service import RetrievalService

app = FastAPI()
retrieval_service = RetrievalService()
mistral_client = MistralClient()


class MistralRequest(BaseModel):
    query: str


@app.post("/generate")
def generate(request: MistralRequest):
    query = request.query
    label = retrieval_service.retrieve_top_k_embeddings(query)
    response = mistral_client.get_response(label)
    return response
