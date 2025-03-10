"""
Ibrahim Nosiru
Date: March 10, 2025


Description:

"""

import os
import json
import time
import requests
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

DB_NAME = os.getenv("DB_NAME", "tecovas_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")

try:
    with psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
    ) as conn:
        conn.autocommit = True
        with conn.cursor() as cur:
            cur.execute("CREATE SCHEMA IF NOT EXISTS staging;")
    logging.info("Schema 'staging' created successfully.")
except Exception as e:
    logging.error(f"Failed to create schema: {e}")
    exit(1)

# Establish SQLAlchemy connection
engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# API Endpoints
API_ENDPOINTS = {
    "orders": "https://fakestoreapi.com/carts",
    "products": "https://fakestoreapi.com/products",
    "users": "https://fakestoreapi.com/users",
}

def fetch_data_with_retry(url, max_retries=5, delay=5, timeout=10):
    """Fetch data from API with retries."""
    session = requests.Session()
    for attempt in range(1, max_retries + 1):
        try:
            response = session.get(url, timeout=timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.warning(f"Attempt {attempt} failed: {e}")
            if attempt < max_retries:
                time.sleep(delay)
            else:
                logging.error(f"Failed to retrieve data from {url} after {max_retries} attempts.")
                return None

# Fetch API data
orders = fetch_data_with_retry(API_ENDPOINTS["orders"])
products = fetch_data_with_retry(API_ENDPOINTS["products"])
users = fetch_data_with_retry(API_ENDPOINTS["users"])

# Validate API responses
if not all([orders, products, users]):
    logging.error("Data retrieval failed. Exiting to prevent incomplete ingestion.")
    exit(1)

# Convert API data to DataFrames
stg_orders = pd.DataFrame([
    {"order_id": cart["id"], "user_id": cart["userId"], "order_date": cart["date"],
     "product_id": item["productId"], "quantity": item["quantity"]}
    for cart in orders for item in cart['products']
])

stg_products = pd.DataFrame(products)
stg_users = pd.DataFrame(users)

# Flatten `rating` field in products
stg_products["rating_rate"] = stg_products["rating"].apply(lambda x: x.get("rate") if isinstance(x, dict) else None)
stg_products["rating_count"] = stg_products["rating"].apply(lambda x: x.get("count") if isinstance(x, dict) else None)
stg_products.drop(columns=["rating"], inplace=True)

# Flatten `name` and `address` in users
stg_users["first_name"] = stg_users["name"].apply(lambda x: x.get("firstname") if isinstance(x, dict) else None)
stg_users["last_name"] = stg_users["name"].apply(lambda x: x.get("lastname") if isinstance(x, dict) else None)
stg_users.drop(columns=["name"], inplace=True)

stg_users["street"] = stg_users["address"].apply(lambda x: x.get("street") if isinstance(x, dict) else None)
stg_users["city"] = stg_users["address"].apply(lambda x: x.get("city") if isinstance(x, dict) else None)
stg_users["zipcode"] = stg_users["address"].apply(lambda x: x.get("zipcode") if isinstance(x, dict) else None)
stg_users.drop(columns=["address"], inplace=True)

# This is to load load data into PostgreSQL (staging schema)
try:
    stg_orders.to_sql("stg_orders", engine, if_exists="append", index=False, schema="staging")
    stg_products.to_sql("stg_products", engine, if_exists="append", index=False, schema="staging")
    stg_users.to_sql("stg_users", engine, if_exists="append", index=False, schema="staging")

    logging.info("Data load complete.")
except Exception as e:
    logging.error(f"Data load failed: {e}")
    exit(1)