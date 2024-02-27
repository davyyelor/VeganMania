import requests
import pandas as pd
import logging

def recipe_search(ingredient):
    app_id_recipe = 'd7ebb8a1'  
    app_key_recipe = '069e3065266fd36a874e3c8aebf06c5c'  
    result = requests.get(
        'https://api.edamam.com/search?q={}&app_id={}&app_key={}'.format(ingredient, app_id_recipe, app_key_recipe)
    )
    data = result.json()
    
    # Extract recipe data
    recipe_list = []
    for hit in data['hits']:
        recipe = hit['recipe']
        recipe_list.append({
            'Recipe': recipe['label'],
            'Ingredients': '\n'.join(recipe['ingredientLines'])
        })
    
    return pd.DataFrame(recipe_list)

def nut_analysis(food):
    app_id = 'f6e716d9'  
    app_key = 'd1abec1a4aafd5edec03531a66177e48' 
    url_req_nutr = 'https://api.edamam.com/api/nutrition-data'

    params_nutr= {
        'app_id': app_id,
        'app_key': app_key,
        'ingr': food
    }
    
    response = requests.get(url_req_nutr, params=params_nutr)

    if response.status_code == 401:
        logging.error('Invalid API Key')

    data = response.json()
    return data

def save_to_dataframe(recipe_df, nut_df):
    recipe_df.to_csv('recipes.csv', index=False)
    nut_df.to_csv('nutritional_analysis.csv', index=False)
    print("Recipes saved to recipes.csv")
    print("Nutritional analysis saved to nutritional_analysis.csv")

if __name__ == "__main__":
    ingredient = '1 apple'
    recipe_data = recipe_search(ingredient)
    nut_data = nut_analysis(ingredient)
    save_to_dataframe(recipe_data, pd.DataFrame([nut_data]))
