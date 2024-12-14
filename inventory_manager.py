# inventory_manager.py
# Gestion des recherches et des rapports

import os

import pandas as pd


class InventoryManager:
    @staticmethod
    def search_product(search_term):
        """
        Recherche un produit ou une catégorie dans l'inventaire consolidé.
        """
        try:
            df = pd.read_csv("data/consolidated_inventory.csv")
        except FileNotFoundError:
            raise FileNotFoundError("Fichier consolidé introuvable. Veuillez d'abord importer les fichiers CSV.")

        results = df[df.apply(lambda row: search_term.lower() in row.to_string().lower(), axis=1)]
        return results

    @staticmethod
    def generate_report(report_type, **kwargs):
        """
        Génère un rapport basé sur le type spécifié.
        """
        try:
            df = pd.read_csv("data/consolidated_inventory.csv")
        except FileNotFoundError:
            raise FileNotFoundError("Fichier consolidé introuvable. Veuillez d'abord importer les fichiers CSV.")

        if report_type == "category":
            category_report = df.groupby("category").agg({"quantity": "sum"}).reset_index()
            os.makedirs("reports", exist_ok=True)
            category_report.to_csv("reports/category_report.csv", index=False)
            return category_report
        elif report_type == "low_stock":
            threshold = kwargs.get("threshold", 5)
            low_stock_report = df[df["quantity"] < threshold].reset_index(drop=True)
            os.makedirs("reports", exist_ok=True)
            low_stock_report.to_csv("reports/low_stock_report.csv", index=False)
            return low_stock_report
        else:
            raise ValueError("Type de rapport non valide.")
