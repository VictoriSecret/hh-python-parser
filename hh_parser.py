import requests
import pandas as pd


def parse_hh_vacancies_api(keyword, pages=2):
    vacancies = []
    url = "https://api.hh.ru/vacancies"

    for page in range(pages):
        params = {
            "text": keyword,
            "page": page,
            "per_page": 100,
            "area": 1,
            "only_with_salary": False
        }

        response = requests.get(url, params=params)
        if response.status_code != 200:
            print(f"Ошибка: {response.status_code}")
            break

        data = response.json()

        for item in data.get("items", []):
            salary = item.get("salary")
            salary_str = "Не указана"
            if salary:
                salary_str = f"{salary.get('from', '')} - {salary.get('to', '')} {salary.get('currency', '')}"

            vacancies.append({
                "title": item.get("name", ""),
                "company": item.get("employer", {}).get("name", ""),
                "salary": salary_str,
                "link": item.get("alternate_url", ""),
                "experience": item.get("experience", {}).get("name", ""),
                "city": item.get("area", {}).get("name", "")
            })

        print(f"Страница {page + 1}: собрано {len(data.get('items', []))} вакансий")

    return vacancies


if __name__ == "__main__":
    data = parse_hh_vacancies_api("Python", pages=2)
    df = pd.DataFrame(data)
    df.to_csv("hh_python_vacancies.csv", index=False, encoding="utf-8-sig")
    print(f"\nВсего собрано: {len(data)} вакансий")