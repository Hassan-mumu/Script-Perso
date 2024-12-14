import glob
import os

import pandas as pd


class CSVManager:
    """
    Classe pour gérer l'importation et la consolidation des fichiers CSV.
    """
    CONSOLIDATED_FILE = "consolidated_inventory.csv"
    REQUIRED_HEADER = "product,quantity,price,category"

    @classmethod
    def import_csv_files(cls, data_path):
        """
        Importe et consolide les fichiers CSV depuis un dossier donné.

        Args:
            data_path (str): Chemin du dossier contenant les fichiers CSV.

        Returns:
            str: Chemin du fichier consolidé, ou None si aucun fichier n'a été consolidé.

        Raises:
            FileNotFoundError: Si aucun fichier CSV n'est trouvé dans le dossier.
            ValueError: Si un fichier CSV a un en-tête invalide.
        """
        print(f"Importation des fichiers CSV depuis : {data_path}")
        csv_files = cls._get_csv_files(data_path)
        output = None

        if not csv_files:
            raise FileNotFoundError(f"Aucun fichier CSV trouvé dans le dossier '{data_path}'.")

        consolidated_data = []
        for file in csv_files:
            try:
                print(f"Lecture et validation du fichier : {file}")
                cls._validate_csv_file(file)
                df = pd.read_csv(file)
                consolidated_data.append(df)
            except Exception as e:
                print(f"Erreur lors de la lecture de {file} : {e}")

        if consolidated_data:
            consolidated_df = pd.concat(consolidated_data, ignore_index=True)
            output_file = os.path.join(data_path, cls.CONSOLIDATED_FILE)
            consolidated_df.to_csv(output_file, index=False)
            print(f"Fichiers consolidés avec succès dans '{output_file}'.")
            output = output_file
        else:
            print("Aucune donnée à consolider.")
        return output

    @staticmethod
    def _get_csv_files(data_path):
        """
        Récupère la liste des fichiers CSV dans un dossier donné.

        Args:
            data_path (str): Chemin du dossier.

        Returns:
            list: Liste des chemins des fichiers CSV.
        """
        return glob.glob(os.path.join(data_path, "*.csv"))

    @classmethod
    def _validate_csv_file(cls, file_path):
        """
        Valide le format d'un fichier CSV en vérifiant son en-tête.

        Args:
            file_path (str): Chemin du fichier CSV.

        Raises:
            ValueError: Si l'en-tête du fichier CSV est invalide.
        """
        with open(file_path, 'r') as f:
            header = f.readline().strip()
            if header != cls.REQUIRED_HEADER:
                raise ValueError(f"Format incorrect pour le fichier {file_path}. "
                                 f"En-tête attendu : '{cls.REQUIRED_HEADER}'.")
