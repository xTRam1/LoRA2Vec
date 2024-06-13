import pickle

import torch
from sentence_transformers import SentenceTransformer

from models import Label


class RetrievalService:
    _EMBEDDING_MODEL = "mixedbread-ai/mxbai-embed-large-v1"
    _N_DIMENSION = 512
    _EMBEDDING__FILES = [
        "embeddings/medical_data_embeddings.pt",
        "embeddings/physics_data_embeddings.pt",
        "embeddings/chemistry_data_embeddings.pt",
        "embeddings/bio_data_embeddings.pt",
    ]
    _CENTROID_FILES = [
        "./centroids/centroids_bio.pt",
        "./centroids/centroids_chemistry.pt",
        "./centroids/centroids_medical.pt",
        "./centroids/centroids_physics.pt",
    ]
    _LABELS_PATH = "labels.pkl"
    _LABELS_PATH_CENTROIDS = "./labels_centroids.pickle"

    _embedding_model: SentenceTransformer
    _all_embeddings: torch.Tensor
    _labels: list

    def __init__(self) -> None:
        self._embedding_model = SentenceTransformer(
            RetrievalService._EMBEDDING_MODEL,
            truncate_dim=RetrievalService._N_DIMENSION,
        )

        # Load all embeddings
        embeddings = []
        for file in RetrievalService._CENTROID_FILES:
            embeddings.append(torch.load(file))
        self._all_embeddings = torch.cat(embeddings)

        with open(RetrievalService._LABELS_PATH_CENTROIDS, "rb") as f:
            self._labels = pickle.load(f)
            # self._labels = [0] * 10 + [1] * 10 + [2] * 10 + [3] * 10
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
