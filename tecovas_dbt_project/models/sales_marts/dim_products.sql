{{ config(materialized='table') }}

SELECT 
    product_id,
    product_name,
    price,
    description,
    category,
    image,
    rating_rate AS rating,
    rating_count
FROM {{ ref('stg_products') }}