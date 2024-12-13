# inventory_manager.py
# Gestion des recherches et des rapports

import pandas as pd

class InventoryManager:
    @staticmethod
    def search_product():
        try:
            df = pd.read_csv("data/consolidated_inventory.csv")
        except FileNotFoundError:
            print("Fichier consolidé introuvable. Veuillez d'abord importer les fichiers CSV.")
            return

        search_term = input("Entrez le nom du produit ou la catégorie à rechercher : ")
        results = df[df.apply(lambda row: search_term.lower() in row.to_string().lower(), axis=1)]

        if results.empty:
            print("Aucun résultat trouvé.")
        else:
            print("Résultats de la recherche :")
            print(results)

    @staticmethod
    def generate_report():
        try:
            df = pd.read_csv("data/consolidated_inventory.csv")
        except FileNotFoundError:
            print("Fichier consolidé introuvable. Veuillez d'abord importer les fichiers CSV.")
            return

        report_choice = input("Générer un rapport par (1) Catégorie ou (2) Produits avec stock faible : ")
        if report_choice == "1":
            category_report = df.groupby("category").agg({"quantity": "sum"})
            print(category_report)
            category_report.to_csv("reports/category_report.csv")
            print("Rapport par catégorie généré dans 'reports/category_report.csv'.")
        elif report_choice == "2":
            threshold = int(input("Entrez le seuil de stock : "))
            low_stock_report = df[df["quantity"] < threshold]
            print(low_stock_report)
            low_stock_report.to_csv("reports/low_stock_report.csv")
            print("Rapport des produits avec stock faible généré dans 'reports/low_stock_report.csv'.")
        else:
            print("Option invalide.")