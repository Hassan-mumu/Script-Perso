# Tests unitaires pour csv_manager
import unittest
from csv_manager import CSVManager
import os
import pandas as pd

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
        if os.path.exists("data/consolidated_inventory.csv"):
            os.remove("data/consolidated_inventory.csv")

    def test_import_csv_files(self):
        CSVManager.import_csv_files()
        self.assertTrue(os.path.exists("data/consolidated_inventory.csv"))
        df = pd.read_csv("data/consolidated_inventory.csv")
        self.assertEqual(len(df), 4)  # Vérifie que 4 lignes sont consolidées

    def test_import_csv_with_missing_file(self):
        os.remove("data/test2.csv")  # Supprime un fichier pour tester
        CSVManager.import_csv_files()
        self.assertTrue(os.path.exists("data/consolidated_inventory.csv"))
        df = pd.read_csv("data/consolidated_inventory.csv")
        self.assertEqual(len(df), 2)  # Vérifie que seules 2 lignes sont consolidées

    def test_import_csv_with_empty_file(self):
        with open("data/empty.csv", "w") as f:
            f.write("product,quantity,price,category\n")  # Fichier vide
        CSVManager.import_csv_files()
        self.assertTrue(os.path.exists("data/consolidated_inventory.csv"))
        df = pd.read_csv("data/consolidated_inventory.csv")
        self.assertEqual(len(df), 4)  # Les lignes des fichiers non vides seulement

    def test_import_csv_invalid_format(self):
        with open("data/invalid.csv", "w") as f:
            f.write("invalid,data,format\n1,2,3\n")  # Fichier non conforme
        CSVManager.import_csv_files()
        self.assertTrue(os.path.exists("data/consolidated_inventory.csv"))
        df = pd.read_csv("data/consolidated_inventory.csv")
        self.assertEqual(len(df), 4)  # Ignore les fichiers invalides

if __name__ == "__main__":
    unittest.main()
