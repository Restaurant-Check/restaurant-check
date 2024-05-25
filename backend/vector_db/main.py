import shutil
import os

from vector_db import RestaurantVectorDB
import json
import matplotlib.pyplot as plt
import numpy as np


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

    """""# LOAD PRECREATED DATABASE

    vecDB = RestaurantVectorDB("./data")
    print("Processing query...")
    db_query_result = vecDB.query("tomato salad")
    for restaurant in db_query_result.restaurants:
        print(json.loads(restaurant.data)["restaurant_name"])
        print(restaurant.highlights)
        print("\n\n")

    # END LOAD PRECREATED DATABASE """""

    # START VISUALIZE DATABASE

    vecDB = RestaurantVectorDB("./data")
    for i, restaurant in enumerate(vecDB.restaurants_db.get_knowledge_base()):
        json_data = json.loads(restaurant)
        n_total_menu_items = sum([len(category['items']) for category in json_data["menu"]])

    restaurants = ['Restaurant A', 'Restaurant B', 'Restaurant C', 'Restaurant D', 'Restaurant E',
                   'Restaurant F', 'Restaurant G', 'Restaurant H', 'Restaurant I', 'Restaurant J']
    menu_items = [20, 15, 30, 25, 10, 45, 35, 40, 28, 18]  # Example numbers of menu items
    sizes = [item * 10 for item in menu_items]  # Scale sizes for better visualization

    # Example data
    restaurants = ['Restaurant A', 'Restaurant B', 'Restaurant C', 'Restaurant D', 'Restaurant E',
                   'Restaurant F', 'Restaurant G', 'Restaurant H', 'Restaurant I', 'Restaurant J']
    menu_items = [20, 15, 30, 25, 10, 45, 35, 40, 28, 18]  # Example numbers of menu items
    sizes = [item * 10 for item in menu_items]  # Scale sizes for better visualization

    # Create a circular layout
    theta = np.linspace(0, 2 * np.pi, len(restaurants), endpoint=False)  # Angle for each restaurant
    r = 10  # Radius of the circle on which restaurants will be placed
    x_coords = r * np.cos(theta)  # X coordinates
    y_coords = r * np.sin(theta)  # Y coordinates

    # Creating the scatter plot (bubble chart)
    plt.figure(figsize=(12, 8))  # Sets the figure size
    plt.scatter(x_coords, y_coords, s=sizes, color='blue', alpha=0.5)

    # Adding labels to each circle
    for i, text in enumerate(restaurants):
        plt.annotate(f"{text}\n{menu_items[i]} items", (x_coords[i], y_coords[i]),
                     textcoords="offset points", xytext=(0, 10), ha='center')

    plt.title('Number of Menu Items per Restaurant Represented by Circle Size')  # Chart title
    plt.axis('equal')  # Ensures the plot is a circle
    plt.xticks([])  # Hide x-axis as it's not meaningful here
    plt.yticks([])  # Hide y-axis as it's not meaningful here
    plt.tight_layout()  # Adjusts plot parameters to give some padding
    plt.show()

    # END VISUALIZE DATABASE


if __name__ == "__main__":
    main()
