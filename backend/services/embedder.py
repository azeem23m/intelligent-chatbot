from dotenv import load_dotenv
import os
import cohere
from fastembed import SparseTextEmbedding


load_dotenv()


class Embedder:

    def __init__(self, model_name: str="embed-multilingual-light-v3.0", dimension: int=384):

        self.client = cohere.Client(os.getenv("COHERE_KEY"))
        self.model_name = model_name
        self.dimension = dimension
        self.sparse_embedder = SparseTextEmbedding("Qdrant/bm25")

    def get_dimension(self):

        return self.dimension

    def embed(self, text: str, input_type: str="search_document"):
        
        dense_embeddings = self.client.embed(
            texts=[text],
            model=self.model_name,
            input_type=input_type,
        ).embeddings[0]

        sparse_embeddings = self.sparse_embedder.query_embed(text)
        
        return dense_embeddings, sparse_embeddings