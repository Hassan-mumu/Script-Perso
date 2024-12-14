# inventory_manager.py
# Gestion des recherches et des rapports

import pandas as pd
import os

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

    @staticmethod
    def run():
        """
        Interface utilisateur pour exécuter les fonctionnalités via la ligne de commande.
        """
        try:
            action = input("Choisissez une action : (1) Rechercher un produit, (2) Générer un rapport : ")
            if action == "1":
                search_term = input("Entrez le nom du produit ou la catégorie à rechercher : ")
                results = InventoryManager.search_product(search_term)
                if results.empty:
                    print("Aucun résultat trouvé.")
                else:
                    print("Résultats de la recherche :")
                    print(results)
            elif action == "2":
                report_choice = input("Générer un rapport par (1) Catégorie ou (2) Produits avec stock faible : ")
                if report_choice == "1":
                    report = InventoryManager.generate_report("category")
                    print("Rapport par catégorie généré avec succès.")
                    print(report)
                elif report_choice == "2":
                    threshold = int(input("Entrez le seuil de stock : "))
                    report = InventoryManager.generate_report("low_stock", threshold=threshold)
                    print("Rapport des produits avec stock faible généré avec succès.")
                    print(report)
                else:
                    print("Option invalide.")
            else:
                print("Action non valide.")
        except Exception as e:
            print(f"Erreur : {e}")
