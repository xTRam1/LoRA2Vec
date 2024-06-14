import pickle
from pathlib import Path

import torch
from sentence_transformers import SentenceTransformer

from models import Label


class RetrievalService:
    _EMBEDDING_MODEL = "mixedbread-ai/mxbai-embed-large-v1"
    _N_DIMENSION = 512

    _embedding_model: SentenceTransformer
    _all_embeddings: torch.Tensor
    _labels: list[Label]

    def __init__(self, embeddings_dir: str) -> None:
        self._embedding_model = SentenceTransformer(
            RetrievalService._EMBEDDING_MODEL,
            truncate_dim=RetrievalService._N_DIMENSION,
        )

        # Load all embeddings and labels
        # Make sure that you have the order of the labels in the same order as the embeddings
        labels = list(Label)
        all_embeddings: dict[Label, torch.Tensor] = {
            label: torch.load(
                f"{embeddings_dir}/{label.value.lower()}_data_embeddings.pt"
            )
            for label in labels
        }
        self._all_embeddings = torch.cat(list(all_embeddings.values()))
        self._labels = [
            label for label in labels for _ in range(all_embeddings[label].shape[0])
        ]

    def retrieve_top_k_embeddings(self, query: str, top_k: int = 5) -> Label:
        """
        Computes the cosine similarity of each embedding to the query and retrieves the top_k most similar embeddings and their labels.

        Parameters:
            query (str): The query to compare against the embeddings.
            top_k (int): The number of top similar embeddings to retrieve.

        Returns:
            Label: The most common label among the top_k most similar embeddings.
        """
        # Generate embedding for the query
        query_embedding = torch.tensor(self._embedding_model.encode([query])[0])

        # Compute cosine similarities
        cosine_similarities = torch.nn.functional.cosine_similarity(
            self._all_embeddings, query_embedding.unsqueeze(0), dim=1
        )

        # Retrieve indices of the top k most similar embeddings
        _, top_k_indices = torch.topk(cosine_similarities, top_k)

        # Select the top_k embeddings and their labels
        top_k_labels = [self._labels[i] for i in top_k_indices]

        # Return the argmax of the labels
        return max(set(top_k_labels), key=top_k_labels.count)
