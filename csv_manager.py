# csv_manager.py
import glob
import os
import re

import pandas as pd


class CSVManager:
    @staticmethod
    def import_csv_files(data_path):
        print(f"Importation des fichiers CSV depuis : {data_path}")
        csv_files = glob.glob(os.path.join(data_path, "*.csv"))
        if not csv_files:
            print(f"Aucun fichier CSV trouvé dans le dossier '{data_path}'.")
            return

        consolidated_data = []
        for file in csv_files:
            try:
                print(f"Lecture du fichier : {file}")
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
            output_file = os.path.join(data_path, "consolidated_inventory.csv")
            consolidated_df.to_csv(output_file, index=False)
            print(f"Fichiers consolidés avec succès dans '{output_file}'.")
        else:
            print("Aucune donnée à consolider.")
