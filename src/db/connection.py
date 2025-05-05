from psycopg2 import connect

from src.config import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER


def get_connection(db: str | None = None):
    return connect(
        dbname=db or DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        client_encoding="UTF8",
    )
