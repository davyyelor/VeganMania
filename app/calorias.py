import requests

class EdamamAPI:
    def __init__(self, app_id, app_key):
        self.app_id = app_id
        self.app_key = app_key
        self.base_url = "https://api.edamam.com/api/nutrition-details"

    def analyze_nutrition(self, data):
        headers = {
            "Content-Type": "application/json",
            "app_id": self.app_id,
            "app_key": self.app_key
        }

        payload = {
            "title": data.get("title", ""),
            "ingr": data.get("ingredients", [])
        }

        response = requests.post(self.base_url, headers=headers, json=payload)

        if response.status_code == 200:
            return response.json()
        else:
            return None

# Reemplaza 'YOUR_APP_ID' y 'YOUR_APP_KEY' con las credenciales reales de tu cuenta Edamam
app_id = '40465ecc'
app_key = '730cd41805be139d5ca7326f86fe23d2'


# Crea una instancia de la clase EdamamAPI
edamam_api = EdamamAPI(app_id, app_key)

# Datos de ejemplo para analizar la nutrición
sample_data = {
    "title": "Sample Recipe",
    "ingredients": ["1 cup rice", "200g chicken breast", "1 cup broccoli"]
}

# Realiza la consulta a la API de Edamam
result = edamam_api.analyze_nutrition(sample_data)

# Imprime el resultado
print(result)
