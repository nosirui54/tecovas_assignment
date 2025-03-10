{{ config(materialized='view') }}

WITH orders AS (
    SELECT * FROM {{ ref('stg_orders') }}
)

SELECT 
    o.order_id,
    o.user_id,
    o.order_date,
    p.product_id,
    o.quantity
FROM orders o
LEFT JOIN {{ ref('stg_products') }} p 
ON o.product_id = p.product_id