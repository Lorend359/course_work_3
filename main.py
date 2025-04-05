from src.api.hh_api import search_employers, get_vacancies_by_employer

if __name__ == "__main__":
    query = "Тинькофф"
    employers = search_employers(query)

    for emp in employers:
        print(f"{emp['id']}: {emp['name']}")

    if employers:
        print("\nПервые 5 вакансий компании:")
        vacancies = get_vacancies_by_employer(employers[0]["id"])
        for v in vacancies[:5]:
            print(f"{v['name']} — {v['alternate_url']}")
