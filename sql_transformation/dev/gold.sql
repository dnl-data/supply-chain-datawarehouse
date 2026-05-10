-- GOLD LAYER : Data Marts

-- Create schemas
CREATE SCHEMA IF NOT EXISTS gold_stock;
CREATE SCHEMA IF NOT EXISTS gold_sales;
CREATE SCHEMA IF NOT EXISTS gold_procurement;

-- =====================================================
-- DATA MART 1 : Stock & Réapprovisionnement
-- =====================================================

-- dim_date (shared dimension)
CREATE OR REPLACE TABLE gold_stock.dim_date AS
SELECT DISTINCT
    snapshot_date AS date,
    EXTRACT(YEAR FROM snapshot_date) AS year,
    EXTRACT(MONTH FROM snapshot_date) AS month,
    EXTRACT(DAY FROM snapshot_date) AS day,
    CASE EXTRACT(MONTH FROM snapshot_date)
        WHEN 1 THEN 'January' WHEN 2 THEN 'February' WHEN 3 THEN 'March'
        WHEN 4 THEN 'April' WHEN 5 THEN 'May' WHEN 6 THEN 'June'
        WHEN 7 THEN 'July' WHEN 8 THEN 'August' WHEN 9 THEN 'September'
        WHEN 10 THEN 'October' WHEN 11 THEN 'November' WHEN 12 THEN 'December'
    END AS month_name,
    EXTRACT(QUARTER FROM snapshot_date) AS quarter
FROM silver.daily_inventory
WHERE snapshot_date IS NOT NULL;

-- dim_product (shared dimension)
CREATE OR REPLACE TABLE gold_stock.dim_product AS
SELECT 
    sku_id,
    product_name,
    category,
    sub_category,
    brand,
    product_type,
    is_active,
    is_discontinued
FROM silver.products;

-- fact_inventory
CREATE OR REPLACE TABLE gold_stock.fact_inventory AS
SELECT 
    di.snapshot_date,
    di.sku_id,
    di.current_stock,
    di.safety_stock,
    di.reorder_point,
    di.daily_sales,
    -- Calculated KPIs
    di.current_stock - di.safety_stock AS stock_vs_safety,
    CASE 
        WHEN di.daily_sales > 0 THEN di.current_stock / di.daily_sales
        ELSE NULL 
    END AS coverage_days,
    di.current_stock < di.reorder_point AS reorder_flag,
    di.incoming_stock,
    di.warehouse_stock,
    di.retail_stock,
    di.amazon_allocated,
    di.tiktokshop_allocated,
    di.zalora_allocated
FROM silver.daily_inventory di;

-- alert_reorder
CREATE OR REPLACE TABLE gold_stock.alert_reorder AS
SELECT 
    snapshot_date,
    sku_id,
    current_stock,
    reorder_point,
    safety_stock,
    'URGENT: Stock below reorder point' AS alert_message
FROM silver.daily_inventory
WHERE current_stock < reorder_point;

-- =====================================================
-- DATA MART 2 : Performance Commerciale
-- =====================================================

-- dim_channel
CREATE OR REPLACE TABLE gold_sales.dim_channel AS
SELECT DISTINCT
    channel,
    CASE channel
        WHEN 'amazon' THEN 'Marketplace'
        WHEN 'tiktokshop' THEN 'Social Commerce'
        WHEN 'zalora' THEN 'Fashion Marketplace'
        WHEN 'retail' THEN 'Physical Store'
        WHEN 'warehouse' THEN 'Direct'
        ELSE 'Other'
    END AS channel_type
FROM silver.sales
WHERE channel IS NOT NULL;

-- dim_promo
CREATE OR REPLACE TABLE gold_sales.dim_promo AS
SELECT DISTINCT
    event_name,
    CASE 
        WHEN event_name IS NULL OR event_name = '' THEN 'No Promotion'
        ELSE 'Promotion'
    END AS promo_type
FROM silver.sales;

-- fact_sales
CREATE OR REPLACE TABLE gold_sales.fact_sales AS
SELECT 
    s.sale_id,
    s.order_id,
    s.date,
    s.sku_id,
    s.channel,
    s.quantity,
    s.unit_price,
    s.discount_pct,
    s.event_name,
    s.customer_segment,
    s.device_type,
    s.payment_method,
    s.returned_flag,
    -- Calculated KPIs
    s.quantity * s.unit_price AS gross_revenue,
    s.quantity * s.unit_price * (s.discount_pct / 100) AS discount_amount,
    s.quantity * s.unit_price * (1 - s.discount_pct / 100) AS net_revenue,
    s.shipping_fee,
    s.voucher_amount,
    s.net_revenue AS net_revenue_clean,
    s.discount_pct > 0 AS promo_flag,
    p.category,
    p.brand
FROM silver.sales s
LEFT JOIN silver.products p ON s.sku_id = p.sku_id;

-- sales_by_channel (aggregated view)
CREATE OR REPLACE TABLE gold_sales.sales_by_channel AS
SELECT 
    channel,
    COUNT(DISTINCT sale_id) AS total_transactions,
    SUM(quantity) AS total_quantity,
    SUM(net_revenue) AS total_revenue,
    AVG(unit_price) AS avg_price,
    AVG(discount_pct) AS avg_discount
FROM silver.sales
GROUP BY channel;

-- =====================================================
-- DATA MART 3 : Achats & Fournisseurs
-- =====================================================

-- dim_supplier
CREATE OR REPLACE TABLE gold_procurement.dim_supplier AS
SELECT 
    supplier_id,
    supplier_name,
    region,
    status,
    lead_time_category
FROM silver.suppliers;

-- fact_purchase
CREATE OR REPLACE TABLE gold_procurement.fact_purchase AS
SELECT 
    po.po_id,
    po.sku_id,
    po.supplier_id,
    po.po_date,
    po.promised_delivery_date,
    po.delivery_date,
    po.order_qty,
    po.unit_cost,
    po.shipping_mode,
    po.status,
    po.incoterm,
    po.currency,
    po.freight_cost,
    po.duty_cost,
    -- Calculated KPIs
    po.order_qty * po.unit_cost AS subtotal_cost,
    po.order_qty * po.unit_cost + po.freight_cost + po.duty_cost AS total_landed_cost,
    EXTRACT(DAY FROM (po.delivery_date - po.po_date)) AS lead_time_days,
    EXTRACT(DAY FROM (po.promised_delivery_date - po.po_date)) AS promised_lead_time_days,
    CASE 
        WHEN po.delivery_date <= po.promised_delivery_date THEN 'On Time'
        ELSE 'Late'
    END AS delivery_performance,
    s.supplier_name,
    s.region,
    p.product_name,
    p.category
FROM silver.purchase_orders po
LEFT JOIN silver.suppliers s ON po.supplier_id = s.supplier_id
LEFT JOIN silver.products p ON po.sku_id = p.sku_id;

-- supplier_performance (aggregated KPIs)
CREATE OR REPLACE TABLE gold_procurement.supplier_performance AS
SELECT 
    supplier_id,
    supplier_name,
    region,
    COUNT(DISTINCT po_id) AS total_orders,
    SUM(order_qty) AS total_quantity_ordered,
    SUM(total_landed_cost) AS total_spent,
    AVG(lead_time_days) AS avg_lead_time_days,
    SUM(CASE WHEN delivery_performance = 'On Time' THEN 1 ELSE 0 END) AS on_time_deliveries,
    ROUND(100.0 * SUM(CASE WHEN delivery_performance = 'On Time' THEN 1 ELSE 0 END) / COUNT(po_id), 2) AS on_time_rate_pct
FROM gold_procurement.fact_purchase
GROUP BY supplier_id, supplier_name, region;

-- =====================================================
-- EXPORTS : Local CSV (for GitHub preview)
-- =====================================================
COPY gold_stock.dim_date TO 'data/dev/gold/dim_date.csv' (HEADER, DELIMITER ',');
COPY gold_stock.dim_product TO 'data/dev/gold/dim_product.csv' (HEADER, DELIMITER ',');
COPY gold_stock.fact_inventory TO 'data/dev/gold/fact_inventory.csv' (HEADER, DELIMITER ',');
COPY gold_stock.alert_reorder TO 'data/dev/gold/alert_reorder.csv' (HEADER, DELIMITER ',');

COPY gold_sales.dim_channel TO 'data/dev/gold/dim_channel.csv' (HEADER, DELIMITER ',');
COPY gold_sales.dim_promo TO 'data/dev/gold/dim_promo.csv' (HEADER, DELIMITER ',');
COPY gold_sales.fact_sales TO 'data/dev/gold/fact_sales.csv' (HEADER, DELIMITER ',');
COPY gold_sales.sales_by_channel TO 'data/dev/gold/sales_by_channel.csv' (HEADER, DELIMITER ',');

COPY gold_procurement.dim_supplier TO 'data/dev/gold/dim_supplier.csv' (HEADER, DELIMITER ',');
COPY gold_procurement.fact_purchase TO 'data/dev/gold/fact_purchase.csv' (HEADER, DELIMITER ',');
COPY gold_procurement.supplier_performance TO 'data/dev/gold/supplier_performance.csv' (HEADER, DELIMITER ',');

-- =====================================================
-- EXPORTS : S3 CSV (for cloud storage)
-- =====================================================
COPY gold_stock.dim_date TO 's3://supply-chain-dwh/test/gold/dim_date.csv' (HEADER, DELIMITER ',');
COPY gold_stock.dim_product TO 's3://supply-chain-dwh/test/gold/dim_product.csv' (HEADER, DELIMITER ',');
COPY gold_stock.fact_inventory TO 's3://supply-chain-dwh/test/gold/fact_inventory.csv' (HEADER, DELIMITER ',');
COPY gold_stock.alert_reorder TO 's3://supply-chain-dwh/test/gold/alert_reorder.csv' (HEADER, DELIMITER ',');

COPY gold_sales.dim_channel TO 's3://supply-chain-dwh/test/gold/dim_channel.csv' (HEADER, DELIMITER ',');
COPY gold_sales.dim_promo TO 's3://supply-chain-dwh/test/gold/dim_promo.csv' (HEADER, DELIMITER ',');
COPY gold_sales.fact_sales TO 's3://supply-chain-dwh/test/gold/fact_sales.csv' (HEADER, DELIMITER ',');
COPY gold_sales.sales_by_channel TO 's3://supply-chain-dwh/test/gold/sales_by_channel.csv' (HEADER, DELIMITER ',');

COPY gold_procurement.dim_supplier TO 's3://supply-chain-dwh/test/gold/dim_supplier.csv' (HEADER, DELIMITER ',');
COPY gold_procurement.fact_purchase TO 's3://supply-chain-dwh/test/gold/fact_purchase.csv' (HEADER, DELIMITER ',');
COPY gold_procurement.supplier_performance TO 's3://supply-chain-dwh/test/gold/supplier_performance.csv' (HEADER, DELIMITER ',');