import requests
import json
from typing import List, Dict, Any
from src.config import HH_API_URL


def search_employers(query: str, per_page: int = 10) -> List[Dict[str, Any]]:
    """
    Ищет компании по ключевому слову.
    Возвращает список работодателей (id, name).
    """
    response = requests.get(f"{HH_API_URL}/employers", params={
        "text": query,
        "per_page": per_page
    })
    response.raise_for_status()
    data = response.json()
    return data.get("items", [])


def get_vacancies_by_employer(employer_id: int, per_page: int = 100) -> List[Dict[str, Any]]:
    """
    Получает вакансии по ID работодателя.
    Возвращает список вакансий.
    """
    response = requests.get(f"{HH_API_URL}/vacancies", params={
        "employer_id": employer_id,
        "per_page": per_page
    })
    response.raise_for_status()
    data = response.json()
    return data.get("items", [])


def get_top_companies() -> None:
    """
    Сохраняет список 10 выбранных компаний (id и name) в файл companies.json.
    """
    company_names = [
        "Яндекс", "Тинькофф", "Сбер", "VK", "Ozon",
        "Wildberries", "Альфа-Банк", "Ростелеком",
        "Касперский", "МТС"
    ]

    companies = []

    for name in company_names:
        results = search_employers(name)
        if results:
            emp = results[0]
            companies.append({
                "id": emp["id"],
                "name": emp["name"]
            })
        else:
            print(f"Компания не найдена: {name}")

    with open("data/companies.json", "w", encoding="utf-8") as f:
        json.dump(companies, f, ensure_ascii=False, indent=2)

    print("✅ Список компаний сохранён в companies.json")
