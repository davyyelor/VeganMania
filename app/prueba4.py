import os

carpeta = 'app\static\images\products'
archivos = os.listdir(carpeta)

print(archivos)
print(len(archivos))