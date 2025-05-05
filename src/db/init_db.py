"""
Модуль инициализации базы: создаёт БД `hh_vacancies`
(если её ещё нет) и таблицы employers + vacancies.
Запускать можно самостоятельно или импортировать из main.py.
"""

from contextlib import closing

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from src.config import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER
from src.db.connection import get_connection


def create_database() -> None:
    """
    Создаёт БД с кодировкой UTF‑8, если она не существует.
    """
    dsn_root = f"dbname=postgres user={DB_USER} password={DB_PASSWORD} " f"host={DB_HOST} port={DB_PORT}"
    with closing(psycopg2.connect(dsn_root)) as conn:
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        with conn.cursor() as cur:
            cur.execute("SELECT 1 FROM pg_database WHERE datname = %s;", (DB_NAME,))
            exists = cur.fetchone()
            if not exists:
                cur.execute(f"CREATE DATABASE {DB_NAME} ENCODING 'UTF8' TEMPLATE template0;")
                print(f"✅ База {DB_NAME} создана")


DDL = """
CREATE TABLE IF NOT EXISTS employers (
    id          INT PRIMARY KEY,
    name        TEXT NOT NULL,
    url         TEXT
);
CREATE TABLE IF NOT EXISTS vacancies (
    id          INT PRIMARY KEY,
    employer_id INT NOT NULL REFERENCES employers(id),
    name        TEXT,
    salary_from INT,
    salary_to   INT,
    url         TEXT
);
"""


def create_tables() -> None:
    """
    Запускает DDL в целевой базе.
    """
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(DDL)
    print("✅ Таблицы employers и vacancies готовы")
