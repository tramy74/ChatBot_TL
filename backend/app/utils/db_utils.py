# backend/app/utils/db_utils.py
import psycopg2
import os

def connect_to_db():
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST", "localhost"),  # Defaults to localhost if not set
        port=os.getenv("DB_PORT", "5432")        # Defaults to 5432 if not set
    )
    return conn
