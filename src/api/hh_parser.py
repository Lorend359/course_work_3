import json

from src.api.hh_api import get_vacancies_by_employer


def collect_all_vacancies() -> None:
    """
    Получает вакансии по списку компаний из data/companies.json
    и сохраняет результат в data/vacancies.json.
    """
    with open("data/companies.json", "r", encoding="utf-8") as f:
        companies = json.load(f)

    all_vacancies = []

    for company in companies:
        print(f"🔍 Получаем вакансии для {company['name']}...")
        vacancies = get_vacancies_by_employer(company["id"])
        for vacancy in vacancies:
            all_vacancies.append(
                {
                    "company_id": company["id"],
                    "company_name": company["name"],
                    "vacancy_name": vacancy["name"],
                    "salary": vacancy["salary"],
                    "url": vacancy["alternate_url"],
                }
            )

    with open("data/vacancies.json", "w", encoding="utf-8") as f:
        json.dump(all_vacancies, f, ensure_ascii=False, indent=2)

    print("✅ Вакансии сохранены в data/vacancies.json")
