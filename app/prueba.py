import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Crear directorios para almacenar las imágenes
os.makedirs("./static/images/in_season", exist_ok=True)
os.makedirs("./static/images/start_of_season", exist_ok=True)
os.makedirs("./static/images/out_of_season", exist_ok=True)

chrome_options = Options()
chrome_options.add_argument("--headless")  # Ejecutar en modo headless
chrome_options.add_argument("--disable-gpu")  # Deshabilitar GPU (mejora la compatibilidad)
chrome_options.add_argument("--no-sandbox")  # Deshabilitar el sandbox (mejora la compatibilidad)
chrome_options.add_argument("--disable-dev-shm-usage")  # Deshabilitar el uso compartido de memoria
chrome_options.add_argument("--start-maximized")  # Iniciar maximizado

# Inicialización del navegador
service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # Acceder a la página
    driver.get("https://soydetemporada.es/")

    # Esperar a que los productos carguen completamente
    wait = WebDriverWait(driver, 20)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "product-item")))

    # Diccionarios para almacenar los productos según su temporada
    in_season = []
    start_of_season = []
    out_of_season = []

    # Obtener todos los elementos de producto
    product_items = driver.find_elements(By.CLASS_NAME, "product-item")

    # Recorrer todos los elementos de producto y clasificarlos según la temporada
    for item in product_items:
        try:
            product_title = item.find_element(By.CLASS_NAME, "product-title").text
            product_image_url = item.find_element(By.TAG_NAME, "img").get_attribute("src")
            season_class = item.get_attribute("class")

            print(f"Procesando: {product_title}")

            if "in-season" in season_class:
                in_season.append((product_title, product_image_url))
            elif "start-of-season" in season_class:
                start_of_season.append((product_title, product_image_url))
            elif "out-of-season" in season_class:
                out_of_season.append((product_title, product_image_url))
        except Exception as e:
            print(f"Error al procesar un elemento: {e}")

    # Función para descargar imágenes
    def download_image(url, path):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                with open(path, 'wb') as f:
                    f.write(response.content)
            else:
                print(f"Error al descargar la imagen: {url}")
        except Exception as e:
            print(f"Error al descargar la imagen: {e}")

    # Descargar imágenes y guardar los productos clasificados
    print("In Season Products:")
    for product_title, product_image_url in in_season:
        print(f"- {product_title}")
        download_image(product_image_url, f"./static/images/in_season/{product_title}.jpg")

    print("\nStart of Season Products:")
    for product_title, product_image_url in start_of_season:
        print(f"- {product_title}")
        download_image(product_image_url, f"./static/images/start_of_season/{product_title}.jpg")

    print("\nOut of Season Products:")
    for product_title, product_image_url in out_of_season:
        print(f"- {product_title}")
        download_image(product_image_url, f"./static/images/out_of_season/{product_title}.jpg")

except Exception as e:
    print(f"Ocurrió un error: {e}")
finally:
    # Cerrar el navegador
    print("Cerrando el navegador...")
    driver.quit()

# Obtener el número de productos clasificados
total_products = len(in_season) + len(start_of_season) + len(out_of_season)
print(f"Número total de productos: {total_products}")
print("Proceso completado.")
