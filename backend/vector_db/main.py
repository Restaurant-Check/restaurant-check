from vector_db import RestaurantVectorDB


def main():
    print("RESTAURANT VECTOR DATABASE")
    vecDB = RestaurantVectorDB("./data")
    #vecDB.insert("I love pizza")
    #vecDB.insert("I love burger")
    print(vecDB.get_knowledge_base())
    vecDB.save()


if __name__ == "__main__":
    main()
