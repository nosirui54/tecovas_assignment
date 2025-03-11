{{ config(materialized='table') }}

WITH orders AS (
    SELECT 
        o.order_id,
        o.user_id,
        CAST(o.order_date AS DATE) AS order_date,
        o.product_id,
        o.quantity AS order_qty,
        p.title AS product_name,
        p.category,
        p.price
    FROM {{ ref('stg_orders') }} AS o
    LEFT JOIN {{ ref('stg_products') }} AS p
    ON o.product_id = p.id
)

SELECT * FROM orders