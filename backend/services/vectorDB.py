from dotenv import load_dotenv
from qdrant_client import QdrantClient, models
from typing import Dict, Any
from .embedder import Embedder


load_dotenv()


class VectorDB():

    def __init__(self, url: str="http://localhost:6333"):

        self.embedder = Embedder()
        self.client = None
        self.url = url
        self.connect()
        self.create_collection("rag")

    def connect(self):
        self.client = QdrantClient(self.url)

    def disconnect(self):
        self.client = None

    def check_connection(self):
        return self.client is not None


    def does_collection_exist(self, collection_name: str):
        return self.client.collection_exists(collection_name=collection_name)

    def create_collection(self, collection_name: str):
        if self.does_collection_exist(collection_name):
            return

        self.client.create_collection(
        collection_name=collection_name,
        vectors_config={
            "dense": models.VectorParams(
                size=self.embedder.get_dimension(), 
                distance=models.Distance.COSINE
            )
        },
        sparse_vectors_config={"sparse": models.SparseVectorParams()},
    )


    def add_document(self, collection_name: str, document: str, metadata: Dict[str, Any], id):

        dense_embeddings, sparse_embeddings = self.embedder.embed(document)

        self.client.upsert(
            collection_name=collection_name,
            points=[
                models.PointStruct(
                    id=id,
                    vector={
                        'dense': dense_embeddings,
                        'sparse': next(sparse_embeddings).as_object()
                    },
                    payload={'metadata': metadata, 'text':document}
                )
            ]
        )


    def query(self, collection_name: str, document: str, limit: int=5):

        dense_embeddings, sparse_embeddings = self.embedder.embed(document, input_type="search_query")

        results = self.client.query_points(
            collection_name=collection_name,
            query=models.FusionQuery(fusion=models.Fusion.RRF),
            prefetch=[
                models.Prefetch(
                    query=dense_embeddings,
                    using="dense",
                    limit=3,
                ),
                models.Prefetch(
                    query=next(sparse_embeddings).as_object(),
                    using="sparse",
                    limit=3,
                ),
            ],
            limit=2,
        ).points

        metadata = [point.payload for point in results]

        return metadata
