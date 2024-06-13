from retrieval_service import RetrievalService
def tester(query):
    retrieval_service = RetrievalService()
    label = retrieval_service.retrieve_top_k_embeddings(query)
    return label

if __name__ == "__main__":
    query = "what is a virus?"
    print(tester(query))