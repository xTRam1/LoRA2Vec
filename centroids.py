import torch
import numpy as np
from sklearn.cluster import KMeans
import pickle

path = './embeddings'
save_path = './centroids'


def centroids(tensor, data_name, n_clusters=10):
    kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(tensor.detach().cpu().numpy())
    centroids_tensor = torch.tensor(kmeans.cluster_centers_)
    torch.save(centroids_tensor, save_path + f'/centroids_{data_name}.pt')
    return centroids_tensor


def save(path, obj):
    with open(path, "wb") as f:
        pickle.dump(obj, f, protocol=pickle.HIGHEST_PROTOCOL)


if __name__ == "__main__":
    dataset = ['bio', 'chemistry', 'medical', 'physics']
    labels = []
    n_cluster = 10
    for data in dataset:
        tensor = torch.load(path + f'/{data}_data_embeddings.pt')
        centers = centroids(tensor, data, n_cluster)
        print(centers.shape)
        labels += [data] * n_cluster
        save('./labels_centroids.pickle', labels)
