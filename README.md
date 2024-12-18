### Guide d'utilisation du programme

Voici comment utiliser les différentes fonctionnalités du programme :

1. **Importation et consolidation des fichiers CSV**
   - Exécutez la commande suivante dans votre terminal :
     ```bash
     python main.py import <chemin_du_dossier>
     ```
   - Remplacez `<chemin_du_dossier>` par le chemin du dossier contenant vos fichiers CSV.
   - Résultat : Tous les fichiers CSV valides seront consolidés dans un fichier unique nommé `consolidated_inventory.csv`.

2. **Recherche de produits ou de catégories**
   - Exécutez la commande suivante :
     ```bash
     python main.py search <terme_de_recherche>
     ```
   - Remplacez `<terme_de_recherche>` par le nom du produit ou de la catégorie que vous souhaitez rechercher.
   - Résultat : Les informations correspondantes s'afficheront directement dans le terminal.

3. **Génération de rapports**
   - **Rapport par catégorie** :
     ```bash
     python main.py report category
     ```
     - Résultat : Un rapport par catégorie sera généré et sauvegardé dans le dossier `reports` sous le nom `category_report.csv`.
   - **Rapport des produits en faible stock** :
     ```bash
     python main.py report low_stock --threshold <seuil>
     ```
     - Remplacez `<seuil>` par le nombre minimal de produits en stock.
     - Résultat : Un rapport des produits ayant un stock inférieur au seuil sera sauvegardé sous le nom `low_stock_report.csv`.


