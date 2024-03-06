from edamamApi import buscar_receta

recetas = buscar_receta('ribs')

recetas = recetas.to_dict(orient='records')

print(recetas)
