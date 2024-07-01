# LoRA2Vec

In the world of LLM applications, there is a growing need for efficient methods to select the best domain-specific model based on a given user query. LoRA2Vec addresses this challenge by creating a robust vector representation of LoRA adapters, enabling dynamic selection during inference.

### Key Features:

***Dataset and Fine-Tuning:*** We curated a dataset of 80,000 question-answer pairs from various domain-specific sources ([chemistry](https://huggingface.co/datasets/camel-ai/chemistry), [physics](https://huggingface.co/datasets/camel-ai/physics
), [medical](https://huggingface.co/datasets/keivalya/MedQuad-MedicalQnADataset
), [biology](https://huggingface.co/datasets/camel-ai/biology
)). Using the Mistral API, we performed LoRA fine-tuning with the Mistral-7B model, simulating a scenario with one base language model and multiple LoRA adapters.

***Embedding and Clustering:*** To represent the LoRA adapters in an embedding space, we used TSNE and PCA projections to observe clustering within their domain-specific dataset. We then applied Kmeans clustering to form centroids, which serve as representative vectors for each dataset and its corresponding fine-tuned LoRA adapter.

***Efficient Inference:*** During inference, the system embeds the user query, calculates cosine similarity with the domain-specific centroids, and retrieves the most relevant LoRA adapter. This approach reduces the total number of query comparisons and the memory footprint of the classification process.

LoRA2Vec is a scalable and efficient method that optimizes the selection of domain-specific models, saving both memory and compute resources.
