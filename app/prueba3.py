from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd

def get_product_info(product):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)

    url = f"https://soydetemporada.es/products/{product}/"
    driver.get(url)

    months_elements = driver.find_elements(By.CSS_SELECTOR, ".month-filter li")
    in_season_months = []
    start_of_season_months = []
    out_of_season_months = []

    for month_element in months_elements:
        month_name = month_element.find_element(By.CLASS_NAME, 'desktop').text
        classes = month_element.get_attribute('class')
        
        if 'in-season' in classes:
            in_season_months.append(month_name)
        elif 'start-of-season' in classes:
            start_of_season_months.append(month_name)
        else:
            out_of_season_months.append(month_name)

    description_element = driver.find_element(By.CSS_SELECTOR, ".panel-body")
    description = description_element.text

    driver.quit()

    return {
        "Producto": product,
        "En Temporada": ", ".join(in_season_months),
        "Inicio Temporada": ", ".join(start_of_season_months),
        "Fuera de Temporada": ", ".join(out_of_season_months),
        "Descripción": description
    }

if __name__ == "__main__":
    productos_info = []

    productos = [
        'acelga', 'aguacate', 'ajo', 'albaricoque', 'alcachofa', 'apio', 'batata',
        'berenjena', 'brocoli', 'calabacin', 'calabaza', 'caqui', 'cardo', 'cebolla',
        'cereza', 'champinon', 'col-de-bruselas', 'col', 'coliflor', 'endibia',
        'esparrago', 'espinaca', 'frambuesa', 'fresa', 'granada', 'guisante', 'haba',
        'higo', 'judia', 'kiwi', 'lechuga', 'lima', 'limon', 'maiz', 'mandarina',
        'manzana', 'melocoton', 'melon', 'mora', 'nabo', 'naranja', 'nectarina',
        'patata', 'pepino', 'pera', 'pimiento', 'platano', 'pomelo', 'puerro',
        'rabano', 'remolacha', 'sandia', 'tomate', 'uva', 'zanahoria'
    ]

    for producto in productos:
        productos_info.append(get_product_info(producto))
        print(f"Producto {producto} guardado.")

    df = pd.DataFrame(productos_info)
