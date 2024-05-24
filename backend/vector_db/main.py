from vector_db import RestaurantVectorDB


def main():
    print("RESTAURANT VECTOR DATABASE")
    vecDB = RestaurantVectorDB()
    vecDB.insert("I love pizza")
    print(vecDB.get_knowledge_base())


if __name__ == "__main__":
    main()
