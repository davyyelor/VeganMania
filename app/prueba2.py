import requests

# URL base de la API
base_url = "https://api.edamam.com/search"

# Parámetros de la consulta
params = {
    "q": "pollo",
    "app_id": "d7ebb8a1",
    "app_key": "069e3065266fd36a874e3c8aebf06c5c",
    "from": 0,
    "to": 3
}

# Realizar la solicitud GET a la API
response = requests.get(base_url, params=params)

# Verificar si la solicitud fue exitosa (código de estado 200)
if response.status_code == 200:
    # Obtener los datos JSON de la respuesta
    data = response.json()
    
    # Iterar sobre los resultados
    for hit in data.get("hits", []):
        recipe = hit.get("recipe")
        print("Receta:", recipe.get("label"))
        print("Ingredientes:")
        for ingredient in recipe.get("ingredients", []):
            print("-", ingredient.get("text"))
        print()
else:
    print("Error al hacer la solicitud:", response.status_code)
