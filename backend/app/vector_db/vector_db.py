import json
import os
import pickle
from dataclasses import dataclass
from typing import List

import faiss
import numpy as np
from openai import OpenAI
from tqdm import tqdm

EMBEDDING_DIM = 1536


def get_embedding(text: str, client, model="text-embedding-3-small", **kwargs) -> List[float]:
    # replace newlines, which can negatively affect performance
    text = text.replace("\n", " ")
    response = client.embeddings.create(input=[text], model=model, **kwargs)

    return response.data[0].embedding


@dataclass
class RestaurantQueryResult:
    data: str  # should be (unparsed) json
    highlights: List[str]  # a list of food items that correspond most to the query


@dataclass
class DatabaseQueryResult:
    restaurants: List[RestaurantQueryResult]


class BasicVectorDB:
    index: faiss.IndexFlatL2  # storing the embedding vectors
    knowledge_base: List  # storing the raw data strings
    client: OpenAI

    def __init__(self):
        self.index = faiss.IndexFlatL2(EMBEDDING_DIM)
        self.knowledge_base = []
        self.client = OpenAI(max_retries=5, api_key=os.environ["CHECK_OPENAI_API_KEY"])

    def insert(self, data: str):
        self.knowledge_base.append(data)
        emb = get_embedding(data, self.client)
        self.index.add(np.array([emb]))

    def query(self, query: str, max_k=3):
        if len(self.knowledge_base) == 0:
            return None

        query_emb = get_embedding(query, self.client)
        _, I = self.index.search(np.array([query_emb]), k=min(len(self.knowledge_base), max_k))
        return [self.knowledge_base[i] for _, i in enumerate(I[0])]

    def get_index(self):
        return self.index

    def set_index(self, index):
        self.index = index

    def get_knowledge_base(self):
        return self.knowledge_base

    def set_knowledge_base(self, knowledge_base):
        self.knowledge_base = knowledge_base

    def is_empty(self):
        return len(self.knowledge_base) == 0


class RestaurantVectorDB:
    restaurants_db: BasicVectorDB                   # storing raw string data of restaurants
    restaurants_menus_dbs: List[BasicVectorDB]      # for each restaurant there is a db storing the menu items
    knowledge_base_path: str
    index_path: str
    data_path: str

    def __init__(self, data_path="./data"):
        self.knowledge_base_path = data_path + "/knowledge_base"
        self.index_path = data_path + "/index.index"
        self.data_path = data_path
        self.restaurants_db = BasicVectorDB()
        self.restaurants_menus_dbs = []

        self.load_data()

    def load_data(self):
        # check if both index and knowledge base files exist
        if os.path.exists(self.index_path) and os.path.exists(self.knowledge_base_path):
            # load restaurants db index
            self.restaurants_db.set_index(faiss.read_index(self.index_path))

            # load restaurants db knowledge base
            with open(self.knowledge_base_path, "rb") as f:
                self.restaurants_db.set_knowledge_base(pickle.load(f))

            # load menu databases
            for i in range(len(self.restaurants_db.get_knowledge_base())):
                restaurant_menu_db = BasicVectorDB()
                restaurant_menu_db.set_index(faiss.read_index(self.data_path + "/menu_index_" + str(i) + ".index"))
                with open(self.data_path + "/menu_knowledge_base_" + str(i), "rb") as f:
                    restaurant_menu_db.set_knowledge_base(pickle.load(f))
                self.restaurants_menus_dbs.append(restaurant_menu_db)

        else:
            print("No existing data directory found")

    def save(self):
        # create data directory if it doesn't exist
        if not os.path.exists(self.data_path):
            os.makedirs(self.data_path)

        # write restaurants db index
        faiss.write_index(self.restaurants_db.get_index(), self.index_path)

        # write restaurants db knowledge base
        with open(self.knowledge_base_path, "wb") as f:
            pickle.dump(self.restaurants_db.get_knowledge_base(), f)

        # write menu databases
        for i, restaurant_menu_db in enumerate(self.restaurants_menus_dbs):
            faiss.write_index(restaurant_menu_db.get_index(), self.data_path + "/menu_index_" + str(i) + ".index")
            with open(self.data_path + "/menu_knowledge_base_" + str(i), "wb") as f:
                pickle.dump(restaurant_menu_db.get_knowledge_base(), f)

    def insert(self, data: str, log=False):
        self.restaurants_db.insert(data.replace("'", "\""))

        # create menu database
        restaurant_menu_db = BasicVectorDB()
        restaurant_json_data = json.loads(data.replace("'", "\""))
        n_total_items = sum([len(category['items']) for category in restaurant_json_data['menu']])
        progress_bar = tqdm(total=n_total_items, desc="Inserting menu items for " + restaurant_json_data["restaurant_name"], colour="green")
        for category in restaurant_json_data['menu']:
            for item in category['items']:
                progress_bar.update(1)
                item_str = category['category'] + ': ' + item['name'] + ' ' + item['description'] + ' | ' + item['price']
                restaurant_menu_db.insert(item_str)

        self.restaurants_menus_dbs.append(restaurant_menu_db)

        if log:
            print("Inserted: ", data)

    def query(self, query: str, max_k=3) -> DatabaseQueryResult:
        if self.restaurants_db.is_empty():
            return DatabaseQueryResult(restaurants=[])

        database_query_result = DatabaseQueryResult(restaurants=[])

        restaurants = self.restaurants_db.query(query, max_k)
        for restaurant_raw_str_data in restaurants:
            # find the food items on the menu which correspond most to the query
            restaurant_menu_db = self.restaurants_menus_dbs[self.restaurants_db.get_knowledge_base().index(restaurant_raw_str_data)]
            highlights = restaurant_menu_db.query(query, max_k)
            database_query_result.restaurants.append(RestaurantQueryResult(data=restaurant_raw_str_data, highlights=highlights))

        return database_query_result

    def get_restaurants_db(self):
        return self.restaurants_db
