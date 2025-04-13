import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# Настройки для работы без лишних окон
chrome_options = Options()
chrome_options.add_argument('--start-maximized')

driver = webdriver.Chrome(options=chrome_options)
url = "https://www.divan.ru/stavropol/category/svet"
driver.get(url)
time.sleep(3)

# Пытаемся найти карточки товаров
luminaires = driver.find_elements(By.CSS_SELECTOR, 'div._Ud0k')
print(f"Найдено товаров: {len(luminaires)}")

parsed_data = []
for luminaire in luminaires:
    try:
        # Название товара
        name = luminaire.find_element(By.CSS_SELECTOR, 'div.lsooF > a > span[itemprop="name"]').text.strip()

        # Цена товара
        price_meta = luminaire.find_element(By.CSS_SELECTOR, 'meta[itemprop="price"]')
        price = price_meta.get_attribute('content')  # Получаем значение атрибута content

        # Ссылка на товар
        link = luminaire.find_element(By.CSS_SELECTOR, 'a.ui-GPFV8').get_attribute('href')

        parsed_data.append([name, price, link])

    except Exception as e:
        print(f"Ошибка в карточке: {e}")
        continue

driver.quit()

# Сохраняем в CSV
with open("svet.csv", 'w', newline='', encoding='utf-8-sig') as file:
    writer = csv.writer(file)
    writer.writerow([' Название товара ', ' Цена ', ' Ссылка на товар '])
    writer.writerows(parsed_data)

print("Готово! Файл сохранён.")
