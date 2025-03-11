{{ config(materialized='table') }}

SELECT 
    id AS product_id,
    title AS product_name,
    price,
    description,
    category,
    image,
    rating_rate AS rating,
    rating_count
FROM {{ ref('stg_products') }}