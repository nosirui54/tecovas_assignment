{{ config(materialized='table') }}

WITH orders AS (
    SELECT 
        o.order_id,
        o.user_id,
        CAST(o.order_date AS DATE) AS order_date,
        o.product_id,
        o.quantity AS order_qty,
        p.product_name,
        p.price,
        p.category
    FROM {{ ref('stg_order_items') }} AS o
    LEFT JOIN {{ ref('stg_products') }} AS p
    ON o.product_id = p.product_id
)

SELECT * FROM orders