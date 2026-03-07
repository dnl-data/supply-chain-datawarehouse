import duckdb
from config import DWH_PATH

conn = duckdb.connect(DWH_PATH)

x = conn.sql("""
    SELECT *
    FROM raw.suppliers
    ;
    """)
print(x)