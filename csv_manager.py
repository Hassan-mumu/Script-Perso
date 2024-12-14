# csv_manager.py
# Gestion des fichiers CSV

import os
import glob
import pandas as pd
import re

class CSVManager:
    @staticmethod
    def import_csv_files():
        print("Importation des fichiers CSV...")
        csv_files = glob.glob("data/*.csv")
        if not csv_files:
            print("Aucun fichier CSV trouvé dans le dossier 'data'.")
            return

        consolidated_data = []
        for file in csv_files:
            try:
                print(f"Lecture du fichier : {file}")
                # Vérification du format avec une regex
                with open(file, 'r') as f:
                    header = f.readline().strip()
                    if not re.match(r'^product,quantity,price,category$', header):
                        raise ValueError(f"Format incorrect pour le fichier {file}")

                df = pd.read_csv(file)
                consolidated_data.append(df)
            except Exception as e:
                print(f"Erreur lors de la lecture de {file} : {e}")

        if consolidated_data:
            consolidated_df = pd.concat(consolidated_data, ignore_index=True)
            consolidated_df.to_csv("data/consolidated_inventory.csv", index=False)
            print("Fichiers consolidés avec succès dans 'data/consolidated_inventory.csv'.")
        else:
            print("Aucune donnée à consolider.")
