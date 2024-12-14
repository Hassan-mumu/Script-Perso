# Tests unitaires pour inventory_manager
import unittest
import os
from inventory_manager import InventoryManager
import pandas as pd

class TestInventoryManager(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.makedirs("data", exist_ok=True)
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
        if os.path.exists("data/consolidated_inventory.csv"):
            os.remove("data/consolidated_inventory.csv")

    def test_search_product(self):
        # Test pour un produit existant
        search_result = InventoryManager.search_product("item1")
        self.assertEqual(len(search_result), 1)
        self.assertEqual(search_result.iloc[0]["product"], "item1")

        # Test pour un produit inexistant
        search_result = InventoryManager.search_product("itemX")
        self.assertTrue(search_result.empty)

    def test_generate_report_by_category(self):
        # Génération de rapport par catégorie
        report = InventoryManager.generate_report("category")
        self.assertTrue(os.path.exists("reports/category_report.csv"))
        expected_data = {
            "category": ["cat1", "cat2"],
            "quantity": [12, 5]
        }
        expected_df = pd.DataFrame(expected_data)
        generated_df = pd.read_csv("reports/category_report.csv")
        pd.testing.assert_frame_equal(generated_df, expected_df)

    def test_generate_report_low_stock(self):
        # Génération de rapport pour stock faible
        threshold = 6
        report = InventoryManager.generate_report("low_stock", threshold=threshold)
        self.assertTrue(os.path.exists("reports/low_stock_report.csv"))
        expected_data = {
            "product": ["item2", "item3"],
            "quantity": [5, 2],
            "price": [200, 50],
            "category": ["cat2", "cat1"]
        }
        expected_df = pd.DataFrame(expected_data)
        generated_df = pd.read_csv("reports/low_stock_report.csv")
        pd.testing.assert_frame_equal(generated_df, expected_df)

if __name__ == "__main__":
    unittest.main()
