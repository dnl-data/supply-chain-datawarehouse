import os
import duckdb
from pathlib import Path
from config import DWH_PATH, DATA_FOLDER


def load_csv_to_duckdb(conn, data_folder):
    """
    Automatically creates DuckDB tables from all CSV files in a folder.

    Args:
        conn (duckdb.Connection): Active DuckDB connection object
        data_folder (str): Path to the folder containing CSV files

    Returns:
        list: Names of all tables successfully created
    """

    created_tables = []

    # create raw schema
    conn.execute("CREATE SCHEMA IF NOT EXISTS raw")

    for csv_file in sorted(Path(data_folder).glob("*.csv")):

        table_name = csv_file.stem.lower().replace(" ", "_")
        csv_path = str(csv_file)

        conn.execute(f"""
            CREATE OR REPLACE TABLE raw.{table_name} AS
            SELECT *
            FROM read_csv_auto('{csv_path}')
        """)

        print(f"Table 'raw.{table_name}' created from {csv_file.name}")

        created_tables.append(f"raw.{table_name}")

    return created_tables


if __name__ == "__main__":

    conn = duckdb.connect(DWH_PATH)

    try:

        tables = load_csv_to_duckdb(conn, DATA_FOLDER)

        if load:
            print(f"{len(load)} tables created successfully: {load}")
        elif os.path.exists(DWH_PATH):
            print("Database file already exists - tables may already be loaded.")
        else:
            print("No tables were created - check your data folder")
    
    except Exception as e:
        print(f"An error occurred during load: {e}")
    
    finally:
        conn.close()
        print("Connection closed.")