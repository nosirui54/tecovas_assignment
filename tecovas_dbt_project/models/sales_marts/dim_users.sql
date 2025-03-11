{{ config(materialized='table') }}

SELECT 
    id AS user_id,
    username,
    email,
    first_name,
    last_name,
    phone,
    street,
    city,
    zipcode
FROM {{ ref('stg_users') }}