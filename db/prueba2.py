import pandas as pd

# Ruta del archivo original
file_path = 'db/recetas_con_imagenes2.csv'

# Cargar el archivo CSV con el delimitador correcto
df = pd.read_csv(file_path, delimiter='|')

# Reemplazar los valores faltantes en la columna 'Tiempo' con '30m'
df['Tiempo'].fillna('30m', inplace=True)

# Reemplazar los valores faltantes en la columna 'Dificultad' con la moda
dificultad_mode = df['Dificultad'].mode()[0]
df['Dificultad'].fillna(dificultad_mode, inplace=True)

# Ruta para guardar el archivo modificado
output_path = 'db/recetas_con_imagenes3.csv'
df.to_csv(output_path, index=False, sep='|')

print(f"Archivo modificado guardado en {output_path}")
