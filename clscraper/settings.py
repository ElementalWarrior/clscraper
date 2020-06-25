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

USER_AGENT = 'Mozilla/5.0 (Linux; Android 10; SM-G975U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.93 Mobile Safari/537.36'

DOWNLOAD_DELAY = 0.25

SPIDER_MODULES = ["clscraper.spiders"]

ROBOTSTXT_OBEY = False

ITEM_PIPELINES = {
    "clscraper.item_pipelines.PostgresPipeline": 300,
}

DUPEFILTER_DEBUG = True
CLOSESPIDER_ERRORCOUNT = 1