# Tests unitaires pour inventory_manager
import os
import unittest
from unittest.mock import patch

import pandas as pd

from inventory_manager import InventoryManager


class TestInventoryManager(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.makedirs("data", exist_ok=True)
        os.makedirs("reports", exist_ok=True)
        data = {
            "product": ["item1", "item2", "item3"],
            "quantity": [10, 5, 2],
            "price": [100, 200, 50],
            "category": ["cat1", "cat2", "cat1"]
        }
        df = pd.DataFrame(data)
        df.to_csv("data/consolidated_inventory.csv", index=False)

    @classmethod
    def tearDownClass(cls):
        for file in ["data/consolidated_inventory.csv", "reports/category_report.csv", "reports/low_stock_report.csv"]:
            if os.path.exists(file):
                os.remove(file)

    def test_search_product(self):
        search_result = InventoryManager.search_product("item1")
        self.assertEqual(len(search_result), 1)
        self.assertEqual(search_result.iloc[0]["product"], "item1")

        search_result = InventoryManager.search_product("itemX")
        self.assertTrue(search_result.empty)

    def test_generate_report_by_category(self):
        report = InventoryManager.generate_report("category")
        self.assertTrue(os.path.exists("reports/category_report.csv"))
        expected_data = {
            "category": ["cat1", "cat2"],
            "quantity": [12, 5]
        }
        expected_df = pd.DataFrame(expected_data)
        pd.testing.assert_frame_equal(report, expected_df)

    def test_generate_report_low_stock(self):
        report = InventoryManager.generate_report("low_stock", threshold=6)
        self.assertTrue(os.path.exists("reports/low_stock_report.csv"))
        expected_data = {
            "product": ["item2", "item3"],
            "quantity": [5, 2],
            "price": [200, 50],
            "category": ["cat2", "cat1"]
        }
        expected_df = pd.DataFrame(expected_data)
        pd.testing.assert_frame_equal(report, expected_df)

    @patch("pandas.read_csv")
    def test_search_product_file_not_found(self, mock_read_csv):
        # Simuler une erreur de fichier introuvable
        mock_read_csv.side_effect = FileNotFoundError
        with self.assertRaises(FileNotFoundError):
            InventoryManager.search_product("test")

    @patch("pandas.read_csv")
    def test_search_product_success(self, mock_read_csv):
        # Simuler un fichier CSV avec des données de test
        mock_df = pd.DataFrame({
            "product": ["Product A", "Product B"],
            "category": ["Category 1", "Category 2"],
            "quantity": [10, 5]
        })
        mock_read_csv.return_value = mock_df
        results = InventoryManager.search_product("Product A")
        self.assertEqual(len(results), 1)
        self.assertEqual(results.iloc[0]["product"], "Product A")

    @patch("pandas.read_csv")
    def test_search_product_no_results(self, mock_read_csv):
        # Simuler un fichier CSV avec des données de test
        mock_df = pd.DataFrame({
            "product": ["Product A", "Product B"],
            "category": ["Category 1", "Category 2"],
            "quantity": [10, 5]
        })
        mock_read_csv.return_value = mock_df
        results = InventoryManager.search_product("Non-existent Product")
        self.assertEqual(len(results), 0)

    @patch("pandas.read_csv")
    def test_generate_report_file_not_found(self, mock_read_csv):
        # Simuler une erreur de fichier introuvable lors de la génération du rapport
        mock_read_csv.side_effect = FileNotFoundError
        with self.assertRaises(FileNotFoundError):
            InventoryManager.generate_report("category")

    @patch("pandas.read_csv")
    @patch("os.makedirs")
    def test_generate_category_report_success(self, mock_makedirs, mock_read_csv):
        # Simuler un fichier CSV avec des données de test pour un rapport par catégorie
        mock_df = pd.DataFrame({
            "category": ["Category 1", "Category 2", "Category 1"],
            "quantity": [10, 5, 3]
        })
        mock_read_csv.return_value = mock_df
        report = InventoryManager.generate_report("category")
        self.assertEqual(len(report), 2)
        self.assertEqual(report.iloc[0]["category"], "Category 1")
        self.assertEqual(report.iloc[0]["quantity"], 13)

    @patch("pandas.read_csv")
    @patch("os.makedirs")
    def test_generate_low_stock_report_success(self, mock_makedirs, mock_read_csv):
        # Simuler un fichier CSV avec des données de test pour un rapport de stocks faibles
        mock_df = pd.DataFrame({
            "product": ["Product A", "Product B", "Product C"],
            "quantity": [10, 3, 2]
        })
        mock_read_csv.return_value = mock_df
        report = InventoryManager.generate_report("low_stock", threshold=5)
        self.assertEqual(len(report), 2)
        self.assertEqual(report.iloc[0]["product"], "Product B")
        self.assertEqual(report.iloc[1]["product"], "Product C")

    @patch("pandas.read_csv")
    def test_generate_report_invalid_type(self, mock_read_csv):
        # Simuler un fichier CSV valide
        mock_df = pd.DataFrame({
            "category": ["Category 1", "Category 2"],
            "quantity": [10, 5]
        })
        mock_read_csv.return_value = mock_df
        with self.assertRaises(ValueError):
            InventoryManager.generate_report("invalid_report_type")


if __name__ == "__main__":
    unittest.main()
