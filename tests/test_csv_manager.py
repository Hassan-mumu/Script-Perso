import os
import tempfile
import unittest
from unittest.mock import patch

import pandas as pd

from csv_manager import CSVManager


class TestCSVManager(unittest.TestCase):
    def setUp(self):
        # Utilisation d'un dossier temporaire pour isoler les tests
        self.test_dir = tempfile.TemporaryDirectory()
        self.data_path = self.test_dir.name
        os.makedirs(self.data_path, exist_ok=True)

        with open(os.path.join(self.data_path, "test1.csv"), "w") as f:
            f.write("product,quantity,price,category\nitem1,10,5,cat1\nitem2,20,15,cat2")
        with open(os.path.join(self.data_path, "test2.csv"), "w") as f:
            f.write("product,quantity,price,category\nitem3,5,25,cat1\nitem4,30,10,cat3")

    def tearDown(self):
        self.test_dir.cleanup()

    def test_import_csv_files(self):
        CSVManager.import_csv_files(self.data_path)
        consolidated_file = os.path.join(self.data_path, "consolidated_inventory.csv")
        self.assertTrue(os.path.exists(consolidated_file))
        df = pd.read_csv(consolidated_file)
        self.assertEqual(len(df), 4)

    def test_import_csv_with_missing_file(self):
        os.remove(os.path.join(self.data_path, "test2.csv"))  # Supprime un fichier pour tester
        CSVManager.import_csv_files(self.data_path)
        consolidated_file = os.path.join(self.data_path, "consolidated_inventory.csv")
        self.assertTrue(os.path.exists(consolidated_file))
        df = pd.read_csv(consolidated_file)
        self.assertEqual(len(df), 2)

    def test_import_csv_with_empty_file(self):
        with open(os.path.join(self.data_path, "empty.csv"), "w") as f:
            f.write("product,quantity,price,category\n")
        CSVManager.import_csv_files(self.data_path)
        consolidated_file = os.path.join(self.data_path, "consolidated_inventory.csv")
        self.assertTrue(os.path.exists(consolidated_file))
        df = pd.read_csv(consolidated_file)
        self.assertEqual(len(df), 4)

    def test_import_csv_invalid_format(self):
        with open(os.path.join(self.data_path, "invalid.csv"), "w") as f:
            f.write("invalid,data,format\n1,2,3\n")
        CSVManager.import_csv_files(self.data_path)
        consolidated_file = os.path.join(self.data_path, "consolidated_inventory.csv")
        self.assertTrue(os.path.exists(consolidated_file))
        df = pd.read_csv(consolidated_file)
        self.assertEqual(len(df), 4)

    @patch("glob.glob")
    @patch("builtins.print")
    def test_import_csv_files_no_csv_found(self, mock_print, mock_glob):
        mock_glob.return_value = []  # Aucun fichier CSV trouvé
        with self.assertRaises(FileNotFoundError) as context:
            CSVManager.import_csv_files(self.data_path)
        self.assertEqual(str(context.exception), f"Aucun fichier CSV trouvé dans le dossier '{self.data_path}'.")

    @patch("glob.glob")
    @patch("pandas.read_csv")
    @patch("builtins.print")
    def test_import_csv_files_no_data_to_consolidate(self, mock_print, mock_read_csv, mock_glob):
        mock_glob.return_value = [os.path.join(self.data_path, "file1.csv"), os.path.join(self.data_path, "file2.csv")]
        mock_read_csv.return_value = pd.DataFrame(columns=["product", "quantity", "price", "category"])
        CSVManager.import_csv_files(self.data_path)
        mock_print.assert_any_call("Aucune donnée à consolider.")
        mock_print.reset_mock()
        mock_glob.reset_mock()


if __name__ == "__main__":
    unittest.main()
