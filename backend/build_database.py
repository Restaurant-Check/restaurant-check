import json

from app.vector_db.vector_db import RestaurantVectorDB

db = RestaurantVectorDB("./app/vector_db/data")

restaurants_data = json.load(open("menu_json/combined.json", "r"))
for restaurant_data in restaurants_data:
    data_str = json.dumps(restaurant_data).replace("'", "")
    print("\n\n\n\nINSERTING:", data_str)
    db.insert(data_str, log=False)

db.save()