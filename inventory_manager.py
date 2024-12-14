# inventory_manager.py
# Gestion des recherches et des rapports

import os
import pandas as pd


class InventoryManager:
    """
    Classe pour gérer les recherches et les rapports d'inventaire.
    """

    DATA_FILE = "data/consolidated_inventory.csv"
    REPORTS_DIR = "reports"

    @classmethod
    def load_inventory(cls):
        """
        Charge l'inventaire consolidé à partir du fichier CSV.
        """
        if not os.path.exists(cls.DATA_FILE):
            raise FileNotFoundError(
                f"Fichier consolidé introuvable : {cls.DATA_FILE}. Veuillez importer les fichiers CSV."
            )
        return pd.read_csv(cls.DATA_FILE)

    @classmethod
    def search_product(cls, search_term):
        """
        Recherche un produit ou une catégorie dans l'inventaire consolidé.

        Args:
            search_term (str): Terme de recherche à utiliser.

        Returns:
            pd.DataFrame: Résultats correspondant au terme de recherche.
        """
        df = cls.load_inventory()
        results = df[df.apply(lambda row: search_term.lower() in row.to_string().lower(), axis=1)]
        return results

    @classmethod
    def generate_report(cls, report_type, **kwargs):
        """
        Génère un rapport basé sur le type spécifié.

        Args:
            report_type (str): Type de rapport à générer ("category", "low_stock", etc.).
            **kwargs: Arguments supplémentaires nécessaires pour certains types de rapports.

        Returns:
            pd.DataFrame: Données du rapport généré.
        """
        df = cls.load_inventory()
        os.makedirs(cls.REPORTS_DIR, exist_ok=True)

        if report_type == "category":
            return cls._generate_category_report(df)
        elif report_type == "low_stock":
            threshold = kwargs.get("threshold", 5)
            return cls._generate_low_stock_report(df, threshold)
        else:
            raise ValueError(f"Type de rapport non valide : {report_type}.")

    @staticmethod
    def _generate_category_report(df):
        """
        Génère un rapport de regroupement par catégorie.

        Args:
            df (pd.DataFrame): Données de l'inventaire.

        Returns:
            pd.DataFrame: Rapport par catégorie.
        """
        category_report = df.groupby("category").agg({"quantity": "sum"}).reset_index()
        file_path = os.path.join(InventoryManager.REPORTS_DIR, "category_report.csv")
        category_report.to_csv(file_path, index=False)
        return category_report

    @staticmethod
    def _generate_low_stock_report(df, threshold):
        """
        Génère un rapport des produits en faible stock.

        Args:
            df (pd.DataFrame): Données de l'inventaire.
            threshold (int): Seuil de faible stock.

        Returns:
            pd.DataFrame: Rapport des produits en faible stock.
        """
        low_stock_report = df[df["quantity"] < threshold].reset_index(drop=True)
        file_path = os.path.join(InventoryManager.REPORTS_DIR, "low_stock_report.csv")
        low_stock_report.to_csv(file_path, index=False)
        return low_stock_report
