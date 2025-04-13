import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
url = "https://tomsk.hh.ru/vacancies/programmist"
driver.get(url)
time.sleep(5)  # Подольше подождать загрузку страницы

# Находим все карточки вакансий
vacancies = driver.find_elements(By.CSS_SELECTOR, 'div.vacancy-card--n77Dj8TY8VIUF0yM')

# Находим все названия компаний
companies = driver.find_elements(By.CSS_SELECTOR, 'span[data-qa="vacancy-serp__vacancy-employer-text"]')

parsed_data = []

for idx, vacancy in enumerate(vacancies):
    try:
        title_element = vacancy.find_element(By.CSS_SELECTOR, 'a.magritte-link___b4rEM_5-0-8')
        title = title_element.text
        link = title_element.get_attribute('href')

        # Берем компанию по индексу
        try:
            company = companies[idx].text
        except IndexError:
            company = "Не указано"

        # Пытаемся найти зарплату
        try:
            salary_element = vacancy.find_element(By.CSS_SELECTOR, 'div.narrow-container--HaV4hduxPuElpx0V span')
            salary = salary_element.text
        except:
            salary = "Не указана"

        parsed_data.append([title, company, salary, link])

    except Exception as e:
        print(f"Ошибка при парсинге: {e}")
        continue

driver.quit()

# Сохраняем в CSV
with open("hh.csv", 'w', newline='', encoding='utf-8-sig') as file:
    writer = csv.writer(file)
    writer.writerow(['Название вакансии', 'Название компании', 'Зарплата', 'Ссылка на вакансию'])
    writer.writerows(parsed_data)

print("✅ Готово! Файл hh.csv сохранен!")


