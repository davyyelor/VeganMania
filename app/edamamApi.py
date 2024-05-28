import requests
import pandas as pd
import logging

# Function to perform nutrition analysis
def nut_analysis(id_nutrition, key_nutrition, query):
    url = 'https://api.edamam.com/api/nutrition-data'
    params = {
        'app_id': id_nutrition,
        'app_key': key_nutrition,
        'ingr': query
    }
    response = requests.get(url, params=params)
    print("Status Code (Nutrition Analysis API):", response.status_code)
    if response.status_code == 401:
        logging.error('{key} - Invalid key (Nutrition Analysis API)'.format(key=key_nutrition))
    return response.json()

# Function to search for recipes
def search_recipe(id_recipes, key_recipes, query):
    url = 'https://api.edamam.com/search?q={query}&app_id={id}&app_key={key}'.format(
        id=id_recipes, key=key_recipes, query=query)
    response = requests.get(url)
    print("Status Code (Recipe Search API) :", response.status_code)
    if response.status_code == 401:
        logging.error('{key} - Invalid key (Recipe Search API)'.format(key=key_recipes))
    return response.json()

# Function to search for food items
def search_food(id_food, key_food, query):
    url = 'https://api.edamam.com/api/food-database/parser?'
    params = {
        'app_id': id_food,
        'app_key': key_food,
        'ingr': query
    }
    response = requests.get(url, params=params)
    print("Status Code (Food Database API):", response.status_code)
    if response.status_code == 401:
        logging.error('{key} - Invalid key (Food Database API)'.format(key=key_food))
    return response.json()

# Function to handle nutrient analysis response
def nutrient_guide(response):
    try:
        df_nutrition = pd.DataFrame(response.get('totalNutrients')).T.rename_axis(str(response.get('ingr')))
        df_total_daily = pd.DataFrame(response.get('totalDaily')).T.rename_axis(str(response.get('ingr')))
        df_total_nut = pd.DataFrame(response.get('totalNutrientsKCal')).T.rename_axis(str(response.get('ingr')))
        nutrient_cal = response.get('calories')
        total_weight = response.get('totalWeight')
        return df_nutrition, df_total_daily, df_total_nut, nutrient_cal, total_weight
    except Exception as e:
        print(e)

# Function to create a DataFrame for food items
def food_table(response):
    try:
        list_foods = [element.get('food').get('label') for element in response.get('hints')]
        list_nutrients = [element.get('food').get('nutrients') for element in response.get('hints')]
        rename_nutrients = ['ENERGY (kcal)', 'PROTEIN (g)', 'FAT (g)', 'CARBS (g)', 'FIBER (g)']
        df_food_table = pd.DataFrame(list_nutrients, index=list_foods).round(2).fillna('Unknown')
        df_food_table.columns = rename_nutrients
        return df_food_table
    except Exception as e:
        print(e)

# Function to write dataframes to files
def write_files(df_nutrition, df_total_daily, df_total_nut, df_recipe, df_food_table, nut_ingredients, query_recipe, query_food):
    path_nutrition = '{Nut}_Nutritional_Analysis.xlsx'.format(Nut=nut_ingredients)
    path_recipe = '{Recipe}_Recipe.csv'.format(Recipe=query_recipe)
    path_food = '{food}_food.csv'.format(food=query_food)
    
    with pd.ExcelWriter(path_nutrition) as writer:
        df_nutrition.to_excel(writer, sheet_name='Nutritional_Analysis')
        df_total_daily.to_excel(writer, sheet_name='Total_Daily')
        df_total_nut.to_excel(writer, sheet_name='totalNutrientsKCal')
    
    df_recipe.to_csv(path_recipe)
    df_food_table.to_csv(path_food)

# Function to search for recipes and save them to a CSV
def buscar_receta(alimento):
    recipes_appkey = '069e3065266fd36a874e3c8aebf06c5c'
    recipes_appid = 'd7ebb8a1'
    data = search_recipe(recipes_appid, recipes_appkey, alimento)
    recipes = []
    for recipe in data['hits']:
        recipe_info = {
            'name': recipe['recipe']['label'],
            'image': recipe['recipe']['image'],
            'recipe_link': recipe['recipe']['url'],
            'diet_labels': ', '.join(recipe['recipe']['dietLabels']),
            'health_labels': ', '.join(recipe['recipe']['healthLabels']),
            'ingredients': recipe['recipe']['ingredientLines']
        }
        recipes.append(recipe_info)

    df = pd.DataFrame(recipes)
    df.to_csv(f"{alimento}_recipes_dataframe.csv", index=False)

# Function to perform nutritional analysis and return a dataframe
def analisis_nutricional(alimento):
    nutrition_appid = 'f6e716d9'
    nutrition_appkey = 'd1abec1a4aafd5edec03531a66177e48'

    response_nut = nut_analysis(nutrition_appid, nutrition_appkey, alimento)

    df_nutrition, df_total_daily, df_total_nut, nutrient_cal, total_weight = nutrient_guide(response_nut)
    return df_nutrition

