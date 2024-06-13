import torch
import numpy as np
from sklearn.cluster import KMeans

path = './embeddings'
save_path = './centroids'


def centroids(tensor, data_name, n_clusters=10):
    kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(tensor.detach().cpu().numpy())
    centroids_tensor = torch.tensor(kmeans.cluster_centers_)
    torch.save(centroids_tensor, save_path + f'/centroids_{data_name}.pt')
    return centroids_tensor


if __name__ == "__main__":
    data = 'physics'
    tensor = torch.load(path + f'/{data}_data_embeddings.pt')
    centers = centroids(tensor, data)
    print(centers.shape)






































































