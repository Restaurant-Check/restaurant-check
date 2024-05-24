from typing import List

import faiss
import numpy as np
from openai import OpenAI
import os

EMBEDDING_DIM = 1536


def get_embedding(text: str, client, model="text-embedding-3-small", **kwargs) -> List[float]:
    # replace newlines, which can negatively affect performance.
    text = text.replace("\n", " ")
    response = client.embeddings.create(input=[text], model=model, **kwargs)

    return response.data[0].embedding


class RestaurantVectorDB:
    _index = faiss.IndexFlatL2()
    knowledge_base = []
    client = None

    def __init__(self):
        self._index = faiss.IndexFlatL2(EMBEDDING_DIM)
        knowledge_base = []
        self._client = OpenAI(max_retries=5, api_key=os.environ["CHECK_OPENAI_API_KEY"])

    def insert(self, data: str):
        self.knowledge_base.append(data)
        emb = get_embedding(data, self._client)
        self._index.add(np.array([emb]))

    def query(self, query: str):
        emb = get_embedding(query, self._client)
        D, I = self._index.search(np.array([emb]), k = min(len(self.knowledge_base), 3))
        return [(self.knowledge_base[i], D[0][j]) for j, i in enumerate(I[0])]

    def get_index(self):
        return self._index

    def get_knowledge_base(self):
        return self.knowledge_base
