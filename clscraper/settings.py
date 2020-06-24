import os

class Config:
    PG_CLIENT_HOST = os.getenv("PG_CLIENT_HOST")
    PG_CLIENT_USERNAME = os.getenv("PG_CLIENT_USERNAME") or "postgres"
    PG_CLIENT_PASSWORD = os.getenv("PG_CLIENT_PASSWORD") or os.getenv("POSTGRES_PASSWORD")
    PG_CLIENT_DB = os.getenv("PG_CLIENT_DB") or "postgres"
    PG_CLIENT_PORT = os.getenv("PG_CLIENT_PORT") or "5432"

    DATABASE = {
        'drivername': 'postgresql',
        'host': PG_CLIENT_HOST,
        'port': PG_CLIENT_PORT,
        'username': PG_CLIENT_USERNAME,
        'password': PG_CLIENT_PASSWORD,
        'database': PG_CLIENT_DB
    }
