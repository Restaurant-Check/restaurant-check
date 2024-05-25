import shutil
import os

from vector_db import RestaurantVectorDB
import json


def main():
    print("RESTAURANT VECTOR DATABASE")

    """"" CREATE DATABASE
    if os.path.exists("./data"):
        shutil.rmtree("./data")

    vecDB = RestaurantVectorDB("./data")

    data_json = json.load(open("example_restaurants_data.json", "r"))
    for restaurant in data_json:
        print("Inserting restaurant", restaurant["restaurant_name"])
        vecDB.insert(str(restaurant))

    print("Processing query...")
    db_query_result = vecDB.query("tenderloin")
    for restaurant in db_query_result.restaurants:
        print(json.loads(restaurant.data)["restaurant_name"])
        print(restaurant.highlights)
        print("\n\n")

    vecDB.save()
    
    END CREATE DATABASE """""

    # LOAD PRECREATED DATABASE

    vecDB = RestaurantVectorDB("./data")
    print("Processing query...")
    db_query_result = vecDB.query("tomato salad")
    for restaurant in db_query_result.restaurants:
        print(json.loads(restaurant.data)["restaurant_name"])
        print(restaurant.highlights)
        print("\n\n")

    # END LOAD PRECREATED DATABASE


if __name__ == "__main__":
    main()
