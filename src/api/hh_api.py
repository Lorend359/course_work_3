import requests
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
