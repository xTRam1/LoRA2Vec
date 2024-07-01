from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sse_starlette import EventSourceResponse

from mistral_client import MistralAPIClient
from models import Label
from retrieval_service import RetrievalService

_EMBEDDINGS_DIR = "50_centroids"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


retrieval_service = RetrievalService(embeddings_dir=_EMBEDDINGS_DIR)
mistral_client = MistralAPIClient()


class MistralClassifyRequest(BaseModel):
    query: str


class MistralGenerateRequest(BaseModel):
    label: Label
    query: str


@app.post("/classify")
def classify(request: MistralClassifyRequest):
    query = request.query
    label = retrieval_service.retrieve_top_k_embeddings(query)
    return {"label": label.value}


@app.post("/generate")
def generate(request: MistralGenerateRequest):
    label = request.label
    query = request.query
    event_stream = mistral_client.chat(query, label)
    return EventSourceResponse(event_stream, ping=600)
