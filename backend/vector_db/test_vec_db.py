import os
import unittest
import shutil

from backend.vector_db.vector_db import RestaurantVectorDB


class MainTest(unittest.TestCase):
    def test_vec_query(self):
        vecDB = RestaurantVectorDB("./tmp")
        vecDB.insert("I love pizza")
        vecDB.insert("I love burger")
        query_result = vecDB.query("pizza")
        print(query_result)
        assert query_result[0][0] == "I love pizza"
        assert query_result[1][0] == "I love burger"
        vecDB.save()
        shutil.rmtree("./tmp")


if __name__ == '__main__':
    unittest.main()
