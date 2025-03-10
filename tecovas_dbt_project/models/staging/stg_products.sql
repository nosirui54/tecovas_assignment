{{ config(materialized='view') }}

SELECT 
    id AS product_id,
    title AS product_name,
    price,
    description,
    category,
    image,
    rating_rate,
    rating_count
FROM {{ source('staging', 'stg_products') }}