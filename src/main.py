from src.api.hh_parser import collect_all_vacancies
from src.db.init_db import create_database, create_tables
from src.db.manager import DBManager
from src.services.loader import load_employers, load_vacancies


def main():
    create_database()
    create_tables()

    db = DBManager()

    while True:
        print(
            "\n1 — Получить вакансии и загрузить в БД\n"
            "2 — Компании и кол-во вакансий\n"
            "3 — Все вакансии\n"
            "4 — Средняя зарплата\n"
            "5 — Вакансии выше средней\n"
            "6 — Поиск вакансий по ключевому слову\n"
            "0 — Выход"
        )
        match input(">> "):
            case "1":
                collect_all_vacancies()
                load_employers()
                load_vacancies()
            case "2":
                for name, cnt in db.get_companies_and_vacancies_count():
                    print(f"{name}: {cnt}")
            case "3":
                for row in db.get_all_vacancies():
                    print(*row, sep=" | ")
            case "4":
                print(db.get_avg_salary() or "нет данных")
            case "5":
                for name, sal in db.get_vacancies_with_higher_salary():
                    print(f"{name}: {sal}")
            case "6":
                kw = input("Ключевое слово: ")
                for name, url in db.get_vacancies_with_keyword(kw):
                    print(name, url)
            case "0":
                break


if __name__ == "__main__":
    main()
