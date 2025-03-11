{{ config(materialized='view') }}

SELECT 
    id,
    username,
    email,
    first_name,
    last_name,
    phone,
    street,
    city,
    zipcode
FROM {{ source('staging', 'stg_users') }}

-- I intentionally removed password field for security reasons