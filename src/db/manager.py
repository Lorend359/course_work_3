"""
Класс‑обёртка над Postgres с пятью методами из ТЗ.
"""

from typing import Any

from src.db.connection import get_connection


class DBManager:
    """Работает с таблицами *employers* и *vacancies*."""

    def _fetch(self, sql: str, *params) -> list[tuple[Any, ...]]:
        with get_connection() as conn, conn.cursor() as cur:
            cur.execute(sql, params)
            return cur.fetchall()

    # 1. Список компаний + кол‑во вакансий
    def get_companies_and_vacancies_count(self) -> list[tuple[str, int]]:
        """Возвратить пары (компания, количество её вакансий)."""
        return self._fetch(
            """
            SELECT e.name, COUNT(v.id)
            FROM employers e
            LEFT JOIN vacancies v ON v.employer_id = e.id
            GROUP BY e.name
            ORDER BY COUNT(v.id) DESC;
            """
        )

    # 2. Все вакансии
    def get_all_vacancies(self) -> list[tuple[str, str, int | None, str]]:
        """Список (компания, вакансия, salary, URL) для всех вакансий."""
        return self._fetch(
            """
            SELECT e.name, v.name, COALESCE(v.salary_from, v.salary_to), v.url
            FROM vacancies v
            JOIN employers e ON e.id = v.employer_id;
            """
        )

    # 3. Средняя зарплата
    def get_avg_salary(self) -> int | None:
        """Среднее значение salary; None, если данных нет."""
        res = self._fetch("SELECT AVG(COALESCE(salary_from, salary_to)) FROM vacancies;")[0][0]
        return int(res) if res else None

    # 4. Вакансии выше средней
    def get_vacancies_with_higher_salary(self) -> list[tuple[str, int]]:
        """Вакансии, у которых salary выше средней по всем вакансиям."""
        return self._fetch(
            """
            SELECT v.name, COALESCE(v.salary_from, v.salary_to)
            FROM vacancies v
            WHERE COALESCE(v.salary_from, v.salary_to) >
                  (SELECT AVG(COALESCE(salary_from, salary_to)) FROM vacancies);
            """
        )

    # 5. Вакансии по ключевому слову
    def get_vacancies_with_keyword(self, keyword: str) -> list[tuple[str, str]]:
        """Вакансии, в названии которых встречается *keyword* (регистронезависимо)."""
        return self._fetch(
            """
            SELECT v.name, v.url
            FROM vacancies v
            WHERE LOWER(v.name) LIKE LOWER(%s);
            """,
            f"%{keyword}%",
        )
