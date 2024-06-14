from fastapi import FastAPI
from pydantic import BaseModel
from sse_starlette import EventSourceResponse

from mistral_client import MistralAPIClient
from retrieval_service import RetrievalService

_EMBEDDINGS_DIR = "50_centroids"

app = FastAPI()
retrieval_service = RetrievalService(embeddings_dir=_EMBEDDINGS_DIR)
mistral_client = MistralAPIClient()


class MistralRequest(BaseModel):
    query: str


@app.post("/generate")
def generate(request: MistralRequest):
    query = request.query
    label = retrieval_service.retrieve_top_k_embeddings(query)
    print(f"Query: {query}, Label: {label.value}")
    event_stream = mistral_client.chat(query, label)
    return EventSourceResponse(event_stream, ping=600)
