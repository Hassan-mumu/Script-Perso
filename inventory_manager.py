# Gestion des recherches et des rapports

import os

import pandas as pd


class InventoryManager:
    @staticmethod
    def search_product(search_term):
        """
        Recherche un produit ou une catégorie dans l'inventaire consolidé.

        Args:
            search_term (str): Le terme à rechercher dans l'inventaire.

        Returns:
            pandas.DataFrame: Un DataFrame contenant les lignes correspondantes à la recherche.

        Raises:
            FileNotFoundError: Si le fichier "data/consolidated_inventory.csv" n'existe pas.
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

        Args:
            report_type (str): Le type de rapport à générer. Peut être "category" ou "low_stock".
            **kwargs: Arguments supplémentaires, comme le seuil de stock pour le rapport "low_stock".

        Returns:
            pandas.DataFrame: Un DataFrame contenant les données du rapport généré.

        Raises:
            FileNotFoundError: Si le fichier "data/consolidated_inventory.csv" n'existe pas.
            ValueError: Si un type de rapport invalide est spécifié.
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
