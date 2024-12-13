# Tests unitaires pour csv_manager
import unittest
from csv_manager import CSVManager
import os

class TestCSVManager(unittest.TestCase):
    def setUp(self):
        os.makedirs("data", exist_ok=True)
        with open("data/test1.csv", "w") as f:
            f.write("product,quantity,price,category\nitem1,10,5,cat1\nitem2,20,15,cat2")
        with open("data/test2.csv", "w") as f:
            f.write("product,quantity,price,category\nitem3,5,25,cat1\nitem4,30,10,cat3")

    def tearDown(self):
        for file in os.listdir("data"):
            os.remove(os.path.join("data", file))

    def test_import_csv_files(self):
        CSVManager.import_csv_files()
        self.assertTrue(os.path.exists("data/consolidated_inventory.csv"))
