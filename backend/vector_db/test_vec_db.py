import unittest

from backend.vector_db.vector_db import RestaurantVectorDB


class MainTest(unittest.TestCase):
    def test_vec_query(self):
        vecDB = RestaurantVectorDB()
        vecDB.insert("I love pizza")
        vecDB.insert("I love burger")
        query_result = vecDB.query("pizza")
        print(query_result)
        assert query_result[0][0] == "I love pizza"
        assert query_result[1][0] == "I love burger"


if __name__ == '__main__':
    unittest.main()
