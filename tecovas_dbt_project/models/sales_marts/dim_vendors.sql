{{ config(materialized='table') }}

SELECT 
    category AS vendor_category,
    COUNT(*) AS product_count
FROM {{ ref('stg_products') }}
GROUP BY category