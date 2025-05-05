import json
from typing import Any

from psycopg2.extras import execute_batch
from src.config import DATA_DIR
from src.db.connection import get_connection

EMPLOYERS_PATH = DATA_DIR / "companies.json"
VACANCIES_PATH = DATA_DIR / "vacancies.json"


def load_employers() -> None:
    """Считать companies.json и вставить записи в таблицу *employers*."""
    with open(EMPLOYERS_PATH, encoding="utf-8") as f:
        items: list[dict[str, Any]] = json.load(f)

    rows = [(int(it["id"]), it["name"], None) for it in items]
    with get_connection() as conn, conn.cursor() as cur:
        execute_batch(
            cur,
            "INSERT INTO employers(id, name, url) VALUES (%s, %s, %s) "
            "ON CONFLICT (id) DO NOTHING;",
            rows,
        )
    print(f"✅ Импортировано работодателей: {len(rows)}")


def load_vacancies() -> None:
    """Считать vacancies.json и вставить записи в таблицу *vacancies*."""
    with open(VACANCIES_PATH, encoding="utf-8") as f:
        items: list[dict[str, Any]] = json.load(f)

    rows = [
        (
            idx,  # временный auto‑id
            int(it["company_id"]),
            it["vacancy_name"],
            (it["salary"] or {}).get("from"),
            (it["salary"] or {}).get("to"),
            it["url"],
        )
        for idx, it in enumerate(items, start=1)
    ]
    with get_connection() as conn, conn.cursor() as cur:
        execute_batch(
            cur,
            "INSERT INTO vacancies(id, employer_id, name, salary_from, salary_to, url) "
            "VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT (id) DO NOTHING;",
            rows,
            page_size=1000,
        )
    print(f"✅ Импортировано вакансий: {len(rows)}")
