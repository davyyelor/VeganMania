import pandas as pd

# Ruta del archivo original
file_path = 'db/recetas_con_imagenes3.csv'

recetas_df = pd.read_csv(file_path, delimiter='|')

# Definir los productos de temporada
productos_temporada = ['acelga', 'frambuesa', 'melón']

# Filtrar las recetas que contienen alguno de los productos de temporada
filtered_recetas_df = recetas_df[recetas_df['Ingredientes'].str.contains('|'.join(productos_temporada), case=False, na=False)]

# Mostrar las recetas filtradas
print(filtered_recetas_df)
