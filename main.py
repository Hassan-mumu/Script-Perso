from csv_manager import CSVManager
from inventory_manager import InventoryManager


def import_csv(data_path):
    """Importer des fichiers CSV depuis un dossier spécifié"""
    try:
        CSVManager.import_csv_files(data_path)
    except Exception as e:
        print(f"Erreur lors de l'importation des fichiers CSV : {e}")


def search_product(search_term):
    """Rechercher un produit ou une catégorie"""
    try:
        results = InventoryManager.search_product(search_term)
        if results.empty:
            print("Aucun résultat trouvé.")
        else:
            print("Résultats de la recherche :")
            print(results)
    except Exception as e:
        print(f"Erreur lors de la recherche : {e}")


def generate_report(report_type, threshold=None):
    """Générer un rapport"""
    try:
        if report_type == "category":
            report = InventoryManager.generate_report("category")
            print("Rapport par catégorie généré avec succès.")
            print(report)
        elif report_type == "low_stock":
            if threshold is None:
                print("Le seuil de stock doit être spécifié pour un rapport sur les stocks faibles.")
            else:
                report = InventoryManager.generate_report("low_stock", threshold=threshold)
                print("Rapport des produits avec stock faible généré avec succès.")
                print(report)
        else:
            print("Type de rapport non valide.")
    except Exception as e:
        print(f"Erreur lors de la génération du rapport : {e}")


def interactive_shell():
    """Boucle interactive pour exécuter les commandes en continu"""
    print("Bienvenue dans le shell interactif du système de gestion d'inventaire.")
    print("Tapez 'help' pour afficher les commandes disponibles. Tapez 'exit' pour quitter.\n")

    while True:
        command = input("inventaire> ").strip().split()

        if not command:
            continue

        action = command[0].lower()

        if action == "exit":
            print("Au revoir !")
            break
        elif action == "help":
            print("\nCommandes disponibles :")
            print("  import <data_path>        Importer les fichiers CSV depuis un dossier spécifié")
            print("  search <search_term>      Rechercher un produit ou une catégorie")
            print("  report category           Générer un rapport par catégorie")
            print("  report low_stock <seuil>  Générer un rapport des produits avec un stock faible")
            print("  exit                      Quitter le programme\n")
        elif action == "import" and len(command) == 2:
            import_csv(command[1])
        elif action == "search" and len(command) >= 2:
            search_term = " ".join(command[1:])
            search_product(search_term)
        elif action == "report" and len(command) >= 2:
            report_type = command[1]
            threshold = int(command[2]) if len(command) == 3 and command[1] == "low_stock" else None
            generate_report(report_type, threshold)
        else:
            print("Commande invalide. Tapez 'help' pour voir les commandes disponibles.")


def main():
    interactive_shell()


if __name__ == "__main__":
    main()
