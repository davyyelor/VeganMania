# Procedimiento para realizar consultas (requests) a la base de datos de EDAMAM mediante sus APIs
# Importar librerías
import pandas as pd
import requests
import json         
import logging

#Claves / ID's de las aplicaciones asignadas
nutrition_appid= 'f6e716d9'
nutrition_appkey= 'd1abec1a4aafd5edec03531a66177e48'
recipes_appid = 'd7ebb8a1'
recipes_appkey= '069e3065266fd36a874e3c8aebf06c5c	'
food_appid= '988976bd'
food_appkey= '6e7b62840e9f82d56b401b80937a8d6d'

# Se define clase Edamam_mcd
class Edamam_mcd:
    "API que regresa datos de tipo json"
    def __init__(self, 
                id_nutrition, 
                key_nutrition, 
                id_recipes,
                key_recipes,
                id_food,
                key_food):
        
        # Asignación de claves / ID de las API's
        self.id_nut = id_nutrition
        self.key_nut = key_nutrition
        self.id_rec = id_recipes
        self.key_rec = key_recipes
        self.id_food = id_food
        self.key_food = key_food
    
    def Nut_Analysis(self, query):
        self.Nut_ingredients = query
        # Se define url (Access Point) para realizar una solicitud a la API Nutrition Analysis
        url_req_nutr = 'https://api.edamam.com/api/nutrition-data'
        # Se definen los parametros a pasar por la función get para realizar la solicitud
        params_nutr= {
            'app_id':self.id_nut,
            'app_key':self.key_nut,
            'ingr':self.Nut_ingredients
            }
        # Envío de solicitud para realizar consulta de análisis nutricional
        Response = requests.get(url_req_nutr, params = params_nutr)

        # Imprimir el código del estatus
        print("Status Code (Nutrition Analysis API):", Response.status_code)
        
        if Response.status_code == 401:
            logging.error('{key} - Clave inválida (Nutrition Analysis API)'.format(key=self.key_nut))

        # Valor de retorno de tipo diccionario, Response tiene contenido JSON serializado
        self.r_Nut = Response.json()
        return self.r_Nut

    def Search_recipe(self, query):
        self.query_recipe = query
        # Se construye url con los parámetros para realizar una solicitd para la busqueda de recetas de un platillo
        url_recipe = 'https://api.edamam.com/search?q={query}&app_id={id}&app_key={key}'.format(id=self.id_rec, key=self.key_rec,query=self.query_recipe)    
        Response = requests.get(url_recipe)

        # Imprimir el código de estatus
        print("Status Code (Recipe Search API) :", Response.status_code)
        
        if Response.status_code == 401:
            logging.error('{key} - Clave inválida (Recipe Search API)'.format(key=self.key_rec))

        # Valor de retorno de tipo diccionario, Response tiene contenido JSON serializado 
        self.r_Recipe = Response.json()
        return self.r_Recipe

    def Search_food(self, query):
        self.query_food = query
        # Se define url (Access Point) para realizar una solicitud de análisis de comida
        url_food = 'https://api.edamam.com/api/food-database/parser?'
        # Se definen los parametros a pasar por la función get para realizar una solicitud
        params_food = {
            'app_id':self.id_food,
            'app_key':self.key_food,
            'ingr':self.query_food
            }
        # Se realiza una solicitud dando la url
        Response = requests.get(url_food, params= params_food)
        
        # Imprimir el código de estatus
        print("Status Code (Food Database API):", Response.status_code)

        if Response.status_code == 401:
            logging.error('{key} - Clave inválida (Food Database API)'.format(key=self.key_rec))

        # Valor de retorno de tipo diccionario, Response tiene contenido JSON serializado
        self.r_Food = Response.json()
        return self.r_Food
    
    # Conjunto de funciones para generar dataframes con los datos principales

    def Nutrient_Guide(self):
        # Manejo de excepciones
        try:
            # Se crean DataFrames de las variables totalNutrients, totalDaily y totalNutrientsKCal 
            self.df_Nutrition= pd.DataFrame(self.r_Nut.get('totalNutrients')).T.rename_axis(str(self.Nut_ingredients))
            self.df_totalDaily = pd.DataFrame(self.r_Nut.get('totalDaily')).T.rename_axis(str(self.Nut_ingredients))
            self.df_total_Nut =  pd.DataFrame(Response_Nut.get('totalNutrientsKCal')).T.rename_axis(str(self.Nut_ingredients))
            # Se obtiene las calorías del alimento
            self.Nutrient_Cal = self.r_Nut.get('calories')
            # Se obtiene el peso total del alimento
            self.totalWeight = self.r_Nut.get('totalWeight')
            
        except Exception as e:
            print(e)
        
    def ingredients_table(self):
        # Manejo de excepciones
        try:
            # Comprensión de listas: se crean nuevas listas con las etiquetas de la receta y con los ingredientes
            list_label = [element_hits.get('recipe').get('label') for element_hits in Response_Recipe.get('hits')]
            list_ingredientes = [element_ingre.get('recipe').get('ingredients') for element_ingre in Response_Recipe.get('hits')]
            # Se construye DataFrame 
            df_ = pd.DataFrame(list_ingredientes, index=list_label).stack().apply(pd.Series).drop(columns=['foodId'])
            self.df_Recipe = df_.rename_axis(["Types", "Items"], axis = "rows").rename(columns = {"foodCategory": "food category", "text":"ingredient name"})

        except Exception as e:
            print(e)

    def food_table(self):
        # Se generar listas vacias
        list_foods = []
        list_nutrients = []
        rename_nutrients = ['ENERGY (kcal)', 'PROTEIN (g)', 'FAT (g)', 'CARBS (g)', 'FIBER (g)']
        # Manejo de excepciones
        try:
            # Comprensión de listas: se crean nuevas listas con las etiquetas de los alimentos y con los nutrientes  
            list_foods = [element.get('food').get('label') for  element in self.r_Food['hints']]
            list_nutrients = [element.get('food').get('nutrients') for element in self.r_Food['hints']]
            # Se construye DataFrame
            self.df_food_table = pd.DataFrame(list_nutrients, index = list_foods).round(2).fillna('Unknown')
            self.df_food_table.columns = rename_nutrients
            
        except Exception as e:
            print(e) 
    
    def write_files(self):
        #  Exportar archivos .CSV/.xlsx
        path_Nutrition = '{Nut}_Nutritional_Analysis.xlsx'.format(Nut=self.Nut_ingredients)
        path_Recipe = '{Recipe}_Recipe.csv'.format(Recipe = self.query_recipe)
        path_food = '{food}_food.csv'.format(food = self.query_food)

        # Se exporta a excel el análisis nutricional 
        with pd.ExcelWriter(path_Nutrition) as writer:
            self.df_Nutrition.to_excel(writer, sheet_name= 'Nutritional_Analysis')
            self.df_totalDaily.to_excel(writer, sheet_name='Total_Daily')
            self.df_total_Nut.to_excel(writer, sheet_name='totalNutrientsKCal')
        # Se exporta en formato CSV los ingredientes de las recetas
        self.df_Recipe.to_csv(path_Recipe)
        # Se exporta en CSV el dataframe con el análisis de los alimentos
        self.df_food_table.to_csv(path_food)



#Claves / ID's de las aplicaciones asignadas
nutrition_appid= 'f6e716d9'
nutrition_appkey= 'd1abec1a4aafd5edec03531a66177e48'
recipes_appid = 'd7ebb8a1'
recipes_appkey= '069e3065266fd36a874e3c8aebf06c5c	'
food_appid= '988976bd'
food_appkey= '6e7b62840e9f82d56b401b80937a8d6d'

# Se crea el objeto EDAMAM_consulta
EDAMAM_consulta = Edamam_mcd(id_nutrition=nutrition_appid, 
                            key_nutrition= nutrition_appkey,
                            id_recipes=recipes_appid,
                            key_recipes=recipes_appkey,
                            id_food=food_appid,
                            key_food=food_appkey)

# Ejercución de los métodos de cada una de las API's para realizar solicitudes
Response_Nut = EDAMAM_consulta.Nut_Analysis(query= '100 gr zucchini lasagna')
Response_Food = EDAMAM_consulta.Search_food(query= 'pizza')
Response_Recipe = EDAMAM_consulta.Search_recipe(query= 'ribs')
# Ejecución de los métodos para obtener los dataframe con los resultados para cada una de las API's
EDAMAM_consulta.Nutrient_Guide()
EDAMAM_consulta.ingredients_table()
EDAMAM_consulta.food_table()
# Se exportan en archivos csv y xlsx los resultados obtenidos
EDAMAM_consulta.write_files()