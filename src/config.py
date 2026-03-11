
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
# 3. Schema and Tables
EXPECTED_SCHEMA = {
    "raw.daily_inventory": {
        "snapshot_date": "DATE",
        "sku_id": "VARCHAR",
        "current_stock": "INTEGER",
        "daily_sales": "INTEGER",
        "incoming_stock": "INTEGER",
        "warehouse_stock": "INTEGER",
        "retail_stock": "INTEGER",
        "amazon_allocated": "INTEGER",
        "tiktokshop_allocated": "INTEGER",
        "zalora_allocated": "INTEGER",
        "reorder_point": "INTEGER",
        "safety_stock": "INTEGER"
    },
    "raw.inventory_snapshot": {
        "snapshot_date": "DATE",
        "sku_id": "VARCHAR",
        "current_stock": "INTEGER",
        "incoming_stock": "INTEGER",
        "stock_age_days": "INTEGER",
        "warehouse_stock": "INTEGER",
        "retail_stock": "INTEGER",
        "amazon_allocated": "INTEGER",
        "tiktokshop_allocated": "INTEGER",
        "zalora_allocated": "INTEGER",
        "reorder_point": "INTEGER",
        "safety_stock": "INTEGER",
        "backorder_qty": "INTEGER",
        "opening_buffer": "INTEGER"
    },
    "raw.products": {
        "sku_id": "VARCHAR",
        "product_name": "VARCHAR",
        "category": "VARCHAR",
        "sub_category": "VARCHAR",
        "brand": "VARCHAR",
        "product_type": "VARCHAR",
        "size_label": "VARCHAR",
        "launch_date": "DATE",
        "shelf_life_months": "DOUBLE",
        "parent_sku": "VARCHAR",
        "default_price": "DOUBLE",
        "primary_supplier_id": "BIGINT",
        "is_active": "BOOLEAN",
        "country_of_origin": "VARCHAR",
        "online_only": "BOOLEAN",
        "avg_rating": "DOUBLE",
        "rating_count": "BIGINT",
        "is_discontinued": "BOOLEAN"
    },
    "raw.purchase_orders": {
        "po_id": "VARCHAR",
        "sku_id": "VARCHAR",
        "supplier_id": "BIGINT",
        "po_date": "DATE",
        "promised_delivery_date": "DATE",
        "delivery_date": "DATE",
        "order_qty": "BIGINT",
        "unit_cost": "DOUBLE",
        "shipping_mode": "VARCHAR",
        "status": "VARCHAR",
        "incoterm": "VARCHAR",
        "currency": "VARCHAR",
        "freight_cost": "DOUBLE",
        "duty_cost": "DOUBLE"
    },
    "raw.sales": {
        "sale_id": "BIGINT",
        "order_id": "VARCHAR",
        "date": "DATE",
        "sku_id": "VARCHAR",
        "channel": "VARCHAR",
        "quantity": "BIGINT",
        "unit_price": "DOUBLE",
        "promo_flag": "BIGINT",
        "discount_pct": "DOUBLE",
        "event_name": "VARCHAR",
        "customer_segment_id": "BIGINT",
        "customer_segment": "VARCHAR",
        "device_type": "VARCHAR",
        "payment_method": "VARCHAR",
        "shipping_fee": "DOUBLE",
        "voucher_amount": "DOUBLE",
        "net_revenue": "DOUBLE",
        "returned_flag": "BOOLEAN",
        "quarter_bucket": "VARCHAR",
        "month": "DATE"
    },
    "raw.suppliers": {
        "supplier_id": "BIGINT",
        "supplier_name": "VARCHAR",
        "region": "VARCHAR",
        "default_shipping_mode": "VARCHAR",
        "status": "VARCHAR",
        "lead_time_category": "VARCHAR",
        "min_order_qty": "BIGINT",
        "contract_start_date": "DATE"
    }
}