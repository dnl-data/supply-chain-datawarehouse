
DWH_PATH = "database/supply_chain.duckdb"
DATA_FOLDER = "data"

structure = """
1. Imports (os, pathlib si nécessaire)

2. Paths & Connexion
   - Chemin vers le fichier DWH
   - Chemin vers le dossier data

3. Schémas & Tables
   - Nom des schémas (raw, clean, etc.)
   - Liste des tables attendues

4. Expected Schema / Data Types
   - Dictionnaire des types attendus par table

5. Null Thresholds
   - Seuils de tolérance de nulls par colonne

6. Conditional Nulls
   - Définition des nulls structurels (condition → colonne)

7. Business Logic Constants
   - Constantes métier utilisées dans les colonnes dérivées
   - Ex: seuils de retard, taux de remise max, etc.
"""
