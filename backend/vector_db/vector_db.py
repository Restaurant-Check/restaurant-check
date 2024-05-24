from typing import List

import faiss
import numpy as np
from openai import OpenAI
import os
import pickle

EMBEDDING_DIM = 1536


def get_embedding(text: str, client, model="text-embedding-3-small", **kwargs) -> List[float]:
    # replace newlines, which can negatively affect performance
    text = text.replace("\n", " ")
    response = client.embeddings.create(input=[text], model=model, **kwargs)

    return response.data[0].embedding


class RestaurantVectorDB:
    _index = faiss.IndexFlatL2()
    knowledge_base = []
    client = None
    knowledge_base_path = ""
    index_path = ""
    data_path = ""

    def __init__(self, data_path="./data"):
        self._index = faiss.IndexFlatL2(EMBEDDING_DIM)
        knowledge_base = []
        self.knowledge_base_path = data_path + "/knowledge_base"
        self.index_path = data_path + "/index.index"
        self.data_path = data_path

        self.load_data()

        self._client = OpenAI(max_retries=5, api_key=os.environ["CHECK_OPENAI_API_KEY"])

    def load_data(self):
        if os.path.exists(self.index_path) and os.path.exists(self.knowledge_base_path):
            self._index = faiss.read_index(self.index_path)
            with open(self.knowledge_base_path, "rb") as f:
                self.knowledge_base = pickle.load(f)

    def save(self):
        if not os.path.exists(self.data_path):
            os.makedirs(self.data_path)

        faiss.write_index(self._index, self.index_path)
        with open(self.knowledge_base_path, "wb") as f:
            pickle.dump(self.knowledge_base, f)

    def insert(self, data: str):
        self.knowledge_base.append(data)
        emb = get_embedding(data, self._client)
        self._index.add(np.array([emb]))
        print("Inserted: ", data)

    def query(self, query: str):
        emb = get_embedding(query, self._client)
        D, I = self._index.search(np.array([emb]), k = min(len(self.knowledge_base), 3))
        return [(self.knowledge_base[i], D[0][j]) for j, i in enumerate(I[0])]

    def get_index(self):
        return self._index

    def get_knowledge_base(self):
        return self.knowledge_base
