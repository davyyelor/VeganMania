import requests
import pandas as pd



def recipe_search(ingredient):
    app_id = 'd7ebb8a1'  # Replace with your Edamam API app ID
    app_key = '069e3065266fd36a874e3c8aebf06c5c'  # Replace with your Edamam API app key
    result = requests.get(
        'https://api.edamam.com/search?q={}&app_id={}&app_key={}'.format(ingredient, app_id, app_key)
    )
    data = result.json()
    return data['hits']

def save_to_dataframe(recipes, ingredient):
    if recipes:
        recipe_list = []

        for recipe in recipes:
            recipe_info = recipe['recipe']
            recipe_name = recipe_info['label']
            recipe_ingredients = "\n".join(recipe_info['ingredientLines'])  # Convertir la lista de ingredientes en una cadena
            recipe_list.append({'Recipe': recipe_name, 'Ingredients': recipe_ingredients})

        df = pd.DataFrame(recipe_list)
        df.to_csv(f"{ingredient}_recipes_dataframe.csv", index=False)
        print(f"Recipes saved to {ingredient}_recipes_dataframe.csv")
    else:
        print("No recipes found")


    
def run(ingredient):
    results = recipe_search(ingredient)
    save_to_dataframe(results, ingredient)

