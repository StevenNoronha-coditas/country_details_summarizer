import psycopg2, os
from psycopg2 import pool, OperationalError

try:
    connection_pool = psycopg2.pool.SimpleConnectionPool(1, 10,
        dbname=os.environ.get("DB_NAME"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASS"),
        host=os.environ.get("DB_HOST"),
        port=os.environ.get("DB_PORT")
    )
except OperationalError as e:
    print(f"Error creating connection pool: {e}")

def get_db_connection():
    try:
        conn = connection_pool.getconn()
        return conn
    except Exception as e:
        print(f"Unable to get connection from pool: {e}")
        return None