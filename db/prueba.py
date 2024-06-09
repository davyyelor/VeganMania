import pandas as pd
import requests
from bs4 import BeautifulSoup

# Paso 1: Cargar el archivo CSV en un DataFrame de pandas
df = pd.read_csv('db/recetas.csv', sep='|')

# Crear una función para obtener la URL de la imagen de cada receta
def get_image_url(recipe_url):
    try:
        response = requests.get(recipe_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            # Buscar la URL de la imagen en la meta etiqueta 'og:image'
            og_image = soup.find('meta', property='og:image')
            if og_image:
                return og_image['content']
    except Exception as e:
        print(f"Error fetching image from {recipe_url}: {e}")
    return None

# Paso 2: Obtener la URL de la imagen para cada receta y eliminar filas sin imagen
total_rows = len(df)
for index, row in df.iterrows():
    image_url = get_image_url(row['Link_receta'])
    if image_url:
        df.at[index, 'images'] = image_url
    print(f"Processing row {index + 1} of {total_rows}")

# Eliminar filas donde no se encontró imagen
df = df.dropna(subset=['images'])

# Mostrar el DataFrame actualizado
print(df)

# Guardar el DataFrame actualizado a un nuevo archivo CSV
df.to_csv('recetas_con_imagenes2.csv', index=False, sep='|')
