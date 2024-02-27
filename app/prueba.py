from edamamApi import Nut_Analysis, Search_recipe, Search_food, Nutrient_Guide, ingredients_table, food_table, write_files, buscarReceta


# Claves / ID's de las aplicaciones asignadas
nutrition_appid = 'f6e716d9'
nutrition_appkey = 'd1abec1a4aafd5edec03531a66177e48'
recipes_appid = 'd7ebb8a1'
recipes_appkey = '069e3065266fd36a874e3c8aebf06c5c'
food_appid = '988976bd'
food_appkey = '6e7b62840e9f82d56b401b80937a8d6d'

print(buscarReceta('chicken'))
