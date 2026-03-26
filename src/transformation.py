import duckdb
import pandas as pd
from config import DWH_PATH,EXPECTED_SCHEMA

conn = duckdb.connect(DWH_PATH)

def verify_table_exist(conn):
    raw_tables = conn.sql("SELECT * FROM {EXPECTED_SCHEMA} WHERE = 'raw'").df()
    for table in tables:
        if tables != raw_tables:
            wrong_table = .append()
            print(f"this tables not imported {wrong_table}")









