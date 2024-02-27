import requests
import pandas as pd
import openpyxl
import logging

def Nut_Analysis(id_nutrition, key_nutrition, query):
    url_req_nutr = 'https://api.edamam.com/api/nutrition-data'
    params_nutr = {
        'app_id': id_nutrition,
        'app_key': key_nutrition,
        'ingr': query
    }
    response = requests.get(url_req_nutr, params=params_nutr)
    print("Status Code (Nutrition Analysis API):", response.status_code)
    if response.status_code == 401:
        logging.error('{key} - Clave inválida (Nutrition Analysis API)'.format(key=key_nutrition))
    return response.json()

def Search_recipe(id_recipes, key_recipes, query):
    url_recipe = 'https://api.edamam.com/search?q={query}&app_id={id}&app_key={key}'.format(
        id=id_recipes, key=key_recipes, query=query)
    response = requests.get(url_recipe)
    print("Status Code (Recipe Search API) :", response.status_code)
    if response.status_code == 401:
        logging.error('{key} - Clave inválida (Recipe Search API)'.format(key=key_recipes))
    return response.json()

def Search_food(id_food, key_food, query):
    url_food = 'https://api.edamam.com/api/food-database/parser?'
    params_food = {
        'app_id': id_food,
        'app_key': key_food,
        'ingr': query
    }
    response = requests.get(url_food, params=params_food)
    print("Status Code (Food Database API):", response.status_code)
    if response.status_code == 401:
        logging.error('{key} - Clave inválida (Food Database API)'.format(key=key_food))
    return response.json()

def Nutrient_Guide(response):
    try:
        df_Nutrition = pd.DataFrame(response.get('totalNutrients')).T.rename_axis(str(response.get('ingr')))
        df_totalDaily = pd.DataFrame(response.get('totalDaily')).T.rename_axis(str(response.get('ingr')))
        df_total_Nut = pd.DataFrame(response.get('totalNutrientsKCal')).T.rename_axis(str(response.get('ingr')))
        Nutrient_Cal = response.get('calories')
        totalWeight = response.get('totalWeight')
        return df_Nutrition, df_totalDaily, df_total_Nut, Nutrient_Cal, totalWeight
    except Exception as e:
        print(e)

def ingredients_table(response):
    try:
        list_label = [element_hits.get('recipe').get('label') for element_hits in response.get('hits')]
        list_ingredientes = [element_ingre.get('recipe').get('ingredients') for element_ingre in response.get('hits')]
        df_ = pd.DataFrame(list_ingredientes, index=list_label).stack().apply(pd.Series).drop(columns=['foodId'])
        df_Recipe = df_.rename_axis(["Types", "Items"], axis="rows").rename(columns={"foodCategory": "food category", "text": "ingredient name"})
        return df_Recipe
    except Exception as e:
        print(e)

def food_table(response):
    try:
        list_foods = []
        list_nutrients = []
        rename_nutrients = ['ENERGY (kcal)', 'PROTEIN (g)', 'FAT (g)', 'CARBS (g)', 'FIBER (g)']
        list_foods = [element.get('food').get('label') for element in response.get('hints')]
        list_nutrients = [element.get('food').get('nutrients') for element in response.get('hints')]
        df_food_table = pd.DataFrame(list_nutrients, index=list_foods).round(2).fillna('Unknown')
        df_food_table.columns = rename_nutrients
        return df_food_table
    except Exception as e:
        print(e)

def write_files(df_Nutrition, df_totalDaily, df_total_Nut, df_Recipe, df_food_table, Nut_ingredients, query_recipe, query_food):
    path_Nutrition = '{Nut}_Nutritional_Analysis.xlsx'.format(Nut=Nut_ingredients)
    path_Recipe = '{Recipe}_Recipe.csv'.format(Recipe=query_recipe)
    path_food = '{food}_food.csv'.format(food=query_food)
    
    with pd.ExcelWriter(path_Nutrition) as writer:
        df_Nutrition.to_excel(writer, sheet_name='Nutritional_Analysis')
        df_totalDaily.to_excel(writer, sheet_name='Total_Daily')
        df_total_Nut.to_excel(writer, sheet_name='totalNutrientsKCal')
    
    df_Recipe.to_csv(path_Recipe)
    df_food_table.to_csv(path_food)

'''
# Claves / ID's de las aplicaciones asignadas
nutrition_appid = 'f6e716d9'
nutrition_appkey = 'd1abec1a4aafd5edec03531a66177e48'
recipes_appid = 'd7ebb8a1'
recipes_appkey = '069e3065266fd36a874e3c8aebf06c5c'
food_appid = '988976bd'
food_appkey = '6e7b62840e9f82d56b401b80937a8d6d'

# Ejercución de los métodos de cada una de las API's para realizar solicitudes
Response_Nut = Nut_Analysis(nutrition_appid, nutrition_appkey, '1 egg')
Response_Food = Search_food(food_appid, food_appkey, 'Peperoni pizza')
Response_Recipe = Search_recipe(recipes_appid, recipes_appkey, 'ribs')

# Ejecución de los métodos para obtener los dataframe con los resultados para cada una de las API's
df_Nutrition, df_totalDaily, df_total_Nut, Nutrient_Cal, totalWeight = Nutrient_Guide(Response_Nut)
df_Recipe = ingredients_table(Response_Recipe)
df_food_table = food_table(Response_Food)

# Escribir archivos
write_files(df_Nutrition, df_totalDaily, df_total_Nut, df_Recipe, df_food_table, '1 egg', 'ribs', 'Peperoni pizza')

print(df_Recipe)
'''