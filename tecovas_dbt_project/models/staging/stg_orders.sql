{{ config(materialized='view') }}

SELECT 
    order_id,
    user_id,
    order_date,
    product_id,
    quantity
FROM {{ source('staging', 'stg_orders') }}