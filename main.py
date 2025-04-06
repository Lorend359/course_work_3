from src.api.hh_api import search_employers, get_vacancies_by_employer, get_top_companies
from src.api.hh_parser import collect_all_vacancies


if __name__ == "__main__":
    print("1. Получить вакансии по компании")
    print("2. Сохранить топ-10 компаний в companies.json")
    print("3. Получить вакансии по companies.json")
    choice = input("Выберите действие: ")

    if choice == "1":
        query = input("Введите название компании: ")
        employers = search_employers(query)

        for emp in employers:
            print(f"{emp['id']}: {emp['name']}")

        if employers:
            print("\nПервые 5 вакансий компании:")
            vacancies = get_vacancies_by_employer(employers[0]["id"])
            for v in vacancies[:5]:
                print(f"{v['name']} — {v['alternate_url']}")
    elif choice == "2":
        get_top_companies()
    elif choice == "3":
        collect_all_vacancies()
    else:
        print("Неверный выбор.")
