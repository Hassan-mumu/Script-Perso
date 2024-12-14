# main.py
# Point d'entrée du programme CLI

from csv_manager import CSVManager
from inventory_manager import InventoryManager


def main():
    print("Bienvenue dans le système de gestion d'inventaire !")
    while True:
        print("\nMenu principal :")
        print("1. Importer des fichiers CSV")
        print("2. Rechercher un produit")
        print("3. Générer un rapport")
        print("4. Quitter")

        choix = input("Choisissez une option : ")
        if choix == "1":
            CSVManager.import_csv_files()
        elif choix == "2":
            terminal_search_product()
        elif choix == "3":
            terminal_generate_report()
        elif choix == "4":
            print("Au revoir !")
            break
        else:
            print("Option invalide. Veuillez réessayer.")


def terminal_search_product():
    """
    Interface utilisateur pour exécuter les fonctionnalités via la ligne de commande.
    """
    try:
        search_term = input("Entrez le nom du produit ou la catégorie à rechercher : ")
        results = InventoryManager.search_product(search_term)
        if results.empty:
            print("Aucun résultat trouvé.")
        else:
            print("Résultats de la recherche :")
            print(results)
    except Exception as e:
        print(f"Erreur : {e}")


def terminal_generate_report():
    try:
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
            print("Action non valide.")
    except Exception as e:
        print(f"Erreur : {e}")


if __name__ == "__main__":
    main()
