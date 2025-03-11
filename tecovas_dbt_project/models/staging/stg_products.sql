{{ config(materialized='view') }}

SELECT 
    id,
    title,
    price,
    description,
    category,
    image,
    rating_rate,
    rating_count
FROM {{ source('staging', 'stg_products') }}