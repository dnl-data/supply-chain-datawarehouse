import duckdb
import pandas as pd
from config import DWH_PATH

conn = duckdb.connect(DWH_PATH)

structure = """0. Vérification existence des tables →
 1. Validation types → 
 2. Validation nulls → 
 3. Colonnes dérivées"""

def verify_table_exist ():




