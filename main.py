import argparse

from csv_manager import CSVManager
from inventory_manager import InventoryManager


def import_csv(data_path):
    """Importer des fichiers CSV depuis un dossier spécifié"""
    CSVManager.import_csv_files(data_path)


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


def parse_args():
    """Parse les arguments de la ligne de commande"""
    parser = argparse.ArgumentParser(description="Système de gestion d'inventaire.")
    subparsers = parser.add_subparsers(dest="command", help="Commandes disponibles")

    # Commande pour importer des fichiers CSV
    import_parser = subparsers.add_parser("import", help="Importer des fichiers CSV")
    import_parser.add_argument("data_path", help="Chemin du dossier contenant les fichiers CSV")

    # Commande pour rechercher un produit
    search_parser = subparsers.add_parser("search", help="Rechercher un produit")
    search_parser.add_argument("search_term", help="Nom du produit ou catégorie à rechercher")

    # Commande pour générer un rapport
    report_parser = subparsers.add_parser("report", help="Générer un rapport")
    report_parser.add_argument("report_type", choices=["category", "low_stock"], help="Type de rapport à générer")
    report_parser.add_argument("--threshold", type=int, help="Seuil de stock pour les produits à faible stock")

    return parser.parse_args()


def main():
    args = parse_args()

    if args.command == "import":
        import_csv(args.data_path)
    elif args.command == "search":
        search_product(args.search_term)
    elif args.command == "report":
        generate_report(args.report_type, args.threshold)
    else:
        print("Commande non valide. Utilisez --help pour afficher les options disponibles.")


if __name__ == "__main__":
    main()
