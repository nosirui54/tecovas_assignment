{{ config(
    materialized='incremental',
    unique_key='order_id'
) }}

SELECT 
    o.order_id,
    o.user_id,
    o.order_date,
    p.product_id,
    p.product_name,
    p.category AS product_category,
    p.price,
    u.username,
    u.email,
    u.first_name || ' ' || u.last_name AS customer_name
FROM {{ ref('fact_orders') }} o
JOIN {{ ref('dim_products') }} p ON o.product_id = p.product_id
JOIN {{ ref('dim_users') }} u ON o.user_id = u.user_id

{% if is_incremental() %}
WHERE o.order_date > (SELECT MAX(order_date) FROM {{ this }})
{% endif %}