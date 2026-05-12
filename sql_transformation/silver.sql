-- Create silver schema
CREATE SCHEMA IF NOT EXISTS silver;


-- SILVER: daily_inventory
CREATE OR REPLACE TABLE silver.daily_inventory AS
SELECT DISTINCT
    snapshot_date,
    LOWER(sku_id) AS sku_id,
    NULLIF(current_stock, 0) AS current_stock,
    NULLIF(daily_sales, 0) AS daily_sales,
    NULLIF(incoming_stock, 0) AS incoming_stock,
    NULLIF(warehouse_stock, 0) AS warehouse_stock,
    NULLIF(retail_stock, 0) AS retail_stock,
    NULLIF(amazon_allocated, 0) AS amazon_allocated,
    NULLIF(tiktokshop_allocated, 0) AS tiktokshop_allocated,
    NULLIF(zalora_allocated, 0) AS zalora_allocated,
    NULLIF(reorder_point, 0) AS reorder_point,
    NULLIF(safety_stock, 0) AS safety_stock
FROM read_csv_auto('s3://supply-chain-dwh/test/bronze/bronze_daily_inventory.csv')
WHERE sku_id IS NOT NULL;


-- SILVER: inventory_snapshot
CREATE OR REPLACE TABLE silver.inventory_snapshot AS
SELECT DISTINCT
    snapshot_date,
    LOWER(sku_id) AS sku_id,
    NULLIF(current_stock, 0) AS current_stock,
    NULLIF(incoming_stock, 0) AS incoming_stock,
    NULLIF(stock_age_days, 0) AS stock_age_days,
    NULLIF(warehouse_stock, 0) AS warehouse_stock,
    NULLIF(retail_stock, 0) AS retail_stock,
    NULLIF(amazon_allocated, 0) AS amazon_allocated,
    NULLIF(tiktokshop_allocated, 0) AS tiktokshop_allocated,
    NULLIF(zalora_allocated, 0) AS zalora_allocated,
    NULLIF(reorder_point, 0) AS reorder_point,
    NULLIF(safety_stock, 0) AS safety_stock,
    NULLIF(backorder_qty, 0) AS backorder_qty,
    NULLIF(opening_buffer, 0) AS opening_buffer
FROM read_csv_auto('s3://supply-chain-dwh/test/bronze/bronze_inventory_snapshot.csv')
WHERE sku_id IS NOT NULL;


-- SILVER: products
CREATE OR REPLACE TABLE silver.products AS
SELECT DISTINCT
    LOWER(sku_id) AS sku_id,
    LOWER(product_name) AS product_name,
    LOWER(category) AS category,
    LOWER(sub_category) AS sub_category,
    LOWER(brand) AS brand,
    LOWER(product_type) AS product_type,
    LOWER(size_label) AS size_label,
    launch_date,
    NULLIF(shelf_life_months, 0) AS shelf_life_months,
    LOWER(parent_sku) AS parent_sku,
    NULLIF(default_price, 0) AS default_price,
    primary_supplier_id,
    is_active,
    LOWER(country_of_origin) AS country_of_origin,
    online_only,
    CASE 
        WHEN avg_rating < 0 THEN 0
        WHEN avg_rating > 5 THEN 5
        ELSE avg_rating
    END AS avg_rating,
    NULLIF(rating_count, 0) AS rating_count,
    is_discontinued
FROM read_csv_auto('s3://supply-chain-dwh/test/bronze/bronze_products.csv')
WHERE sku_id IS NOT NULL;


-- SILVER: purchase_orders
CREATE OR REPLACE TABLE silver.purchase_orders AS
SELECT DISTINCT
    LOWER(po_id) AS po_id,
    LOWER(sku_id) AS sku_id,
    supplier_id,
    po_date,
    promised_delivery_date,
    delivery_date,
    NULLIF(order_qty, 0) AS order_qty,
    NULLIF(unit_cost, 0) AS unit_cost,
    LOWER(shipping_mode) AS shipping_mode,
    LOWER(status) AS status,
    LOWER(incoterm) AS incoterm,
    LOWER(currency) AS currency,
    NULLIF(freight_cost, 0) AS freight_cost,
    NULLIF(duty_cost, 0) AS duty_cost
FROM read_csv_auto('s3://supply-chain-dwh/test/bronze/bronze_purchase_orders.csv')
WHERE po_id IS NOT NULL;


-- SILVER: sales
CREATE OR REPLACE TABLE silver.sales AS
SELECT DISTINCT
    sale_id,
    LOWER(order_id) AS order_id,
    date,
    LOWER(sku_id) AS sku_id,
    LOWER(channel) AS channel,
    NULLIF(quantity, 0) AS quantity,
    NULLIF(unit_price, 0) AS unit_price,
    promo_flag,
    CASE 
        WHEN discount_pct < 0 THEN 0
        WHEN discount_pct > 100 THEN 100
        ELSE discount_pct
    END AS discount_pct,
    LOWER(event_name) AS event_name,
    customer_segment_id,
    LOWER(customer_segment) AS customer_segment,
    LOWER(device_type) AS device_type,
    LOWER(payment_method) AS payment_method,
    NULLIF(shipping_fee, 0) AS shipping_fee,
    voucher_amount,
    NULLIF(net_revenue, 0) AS net_revenue,
    returned_flag,
    LOWER(quarter_bucket) AS quarter_bucket,
    month
FROM read_csv_auto('s3://supply-chain-dwh/test/bronze/bronze_sales.csv')
WHERE sale_id IS NOT NULL;

-- SILVER: suppliers
CREATE OR REPLACE TABLE silver.suppliers AS
SELECT DISTINCT
    supplier_id,
    LOWER(supplier_name) AS supplier_name,
    LOWER(region) AS region,
    LOWER(default_shipping_mode) AS default_shipping_mode,
    LOWER(status) AS status,
    LOWER(lead_time_category) AS lead_time_category,
    CASE 
        WHEN min_order_qty <= 0 THEN NULL
        ELSE min_order_qty
    END AS min_order_qty,
    contract_start_date
FROM read_csv_auto('s3://supply-chain-dwh/test/bronze/bronze_suppliers.csv')
WHERE supplier_id IS NOT NULL;

-- EXPORT: S3 CSV (for cloud storage)
COPY silver.daily_inventory TO 's3://supply-chain-dwh/test/silver/silver_daily_inventory.csv' (HEADER, DELIMITER ',');
COPY silver.inventory_snapshot TO 's3://supply-chain-dwh/test/silver/silver_inventory_snapshot.csv' (HEADER, DELIMITER ',');
COPY silver.products TO 's3://supply-chain-dwh/test/silver/silver_products.csv' (HEADER, DELIMITER ',');
COPY silver.purchase_orders TO 's3://supply-chain-dwh/test/silver/silver_purchase_orders.csv' (HEADER, DELIMITER ',');
COPY silver.sales TO 's3://supply-chain-dwh/test/silver/silver_sales.csv' (HEADER, DELIMITER ',');
COPY silver.suppliers TO 's3://supply-chain-dwh/test/silver/silver_suppliers.csv' (HEADER, DELIMITER ',');