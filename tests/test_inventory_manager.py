# Tests unitaires pour inventory_manager
import unittest
import os
from inventory_manager import InventoryManager
import pandas as pd

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

if __name__ == "__main__":
    unittest.main()
