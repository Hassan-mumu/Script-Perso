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
            InventoryManager.search_product()
        elif choix == "3":
            InventoryManager.generate_report()
        elif choix == "4":
            print("Au revoir !")
            break
        else:
            print("Option invalide. Veuillez réessayer.")

if __name__ == "__main__":
    main()

