import torch
import numpy as np
from sklearn.cluster import KMeans
import pickle
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA

def find_centroid_indices(data, centroids):
    """
    Find the indices of centroids in the original dataset.

    Parameters:
    data (np.ndarray): The original dataset.
    centroids (np.ndarray): The centroids found by KMeans.

    Returns:
    list: The indices of the centroids in the original dataset.
    """
    indices = []
    for centroid in centroids:
        distances = np.linalg.norm(data - centroid, axis=1)
        centroid_index = np.argmin(distances)
        indices.append(centroid_index)
    return np.array(indices)

def plot_tsne_centers_and_data(tensor, data, n_clusters=10):
    print(f"plotting {data}")
    array = tensor.detach().cpu().numpy()
    kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(array)
    centroids = kmeans.cluster_centers_
    print("TSNE Begining")
    print(array.shape)
    tsne = PCA(n_components=2)
    array_tsne = tsne.fit_transform(array)

    # Step 5: Perform t-SNE on the centroids with reduced perplexity
    # tsne_centroids = TSNE(n_components=2, perplexity=5, random_state=0)
    # centroids_tsne = tsne.fit_transform(centroids)
    # print(kmeans.labels_)
    indices = find_centroid_indices(array, centroids)
    centroids_tsne = np.array([array_tsne[x] for x in indices])
    print(centroids_tsne.shape)
    print("TSNE end")

    plt.figure(figsize=(100, 80))
    plt.scatter(array_tsne[:, 0], array_tsne[:, 1], c='blue', alpha=0.5, label='Training Data')
    plt.scatter(centroids_tsne[:, 0], centroids_tsne[:, 1], c='red', marker='X', s=200, label='Centroids')
    plt.legend()
    plt.title('t-SNE Visualization of Training Data and KMeans Centroids')
    plt.xlabel('t-SNE Component 1')
    plt.ylabel('t-SNE Component 2')
    # plt.show()
    plt.savefig('visual' + data + '.pdf', format='pdf')
    plt.show()
    return torch.tensor(centroids)


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
        centers = plot_tsne_centers_and_data(tensor, data, n_cluster)
        centers = centroids(tensor, data, n_cluster)
        print(centers.shape)
        labels += [data] * n_cluster
        save('./labels_centroids.pickle', labels)
