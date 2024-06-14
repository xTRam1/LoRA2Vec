import argparse
import os
import pickle

import torch
from sklearn.cluster import KMeans

from models import Label

save_path = "centroids/"


def centroids(tensor: torch.Tensor, data_name: str, n_clusters: int) -> torch.Tensor:
    kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(
        tensor.detach().cpu().numpy()
    )
    centroids_tensor = torch.tensor(kmeans.cluster_centers_)
    os.makedirs(f"{n_clusters}_centroids", exist_ok=True)
    torch.save(
        centroids_tensor, f"{n_clusters}_centroids/{data_name}_data_embeddings.pt"
    )
    return centroids_tensor


if __name__ == "__main__":
    dataset: list[str] = list(Label._value2member_map_.keys())
    print(dataset)

    parser = argparse.ArgumentParser()
    parser.add_argument("--n_clusters", type=int, required=True)
    args = parser.parse_args()

    for data in dataset:
        data_name = data.lower()
        tensor = torch.load(f"embeddings/{data_name}_data_embeddings.pt")
        centers = centroids(tensor, data_name, args.n_clusters)
