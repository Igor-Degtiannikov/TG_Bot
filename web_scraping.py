import requests
from bs4 import BeautifulSoup
import re

url = 'https://www.jobs.cz/prace/praha/it-analytik/?locality%5Bradius%5D=0' # Указываем url страницу

response = requests.get(url) # Отправляет запрос к указанному url и возвращаем response
if response.status_code == 200: # переменная, хранится ответ от сервера, а также состояние кода запроса(200)
    soup = BeautifulSoup(response.text, 'html.parser') # Создает обьект, и испоьзует парсер для анализа

    salary_elements = soup.find_all('span', class_='Tag Tag--success Tag--small Tag--subtle') # Находим все элементы
    salaries = [] # Добовляем среднее значение зарплат в пустой список
    for element in salary_elements:
        salary_text = element.get_text(strip=True)
        salary_numbers = re.findall(r'\d+\s?\d*', salary_text)  # Находим все числа в тексте

        if len(salary_numbers) == 2:
            min_salary = int(salary_numbers[0].replace('\xa0', '').replace(' ', ''))
            max_salary = int(salary_numbers[1].replace('\xa0', '').replace(' ', ''))

            average_salary = (min_salary + max_salary) / 2
            salaries.append(average_salary)

    if salaries:
        overall_average_salary = sum(salaries) / len(salaries)
        print(f"Средняя зарплата аналитика данных: {overall_average_salary:.2f} CZK")
    else:
        print("Не удалось найти информацию о зарплатах.")
else:
    print("Ошибка загрузки страницы.")








