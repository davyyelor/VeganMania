from edamamApi import buscar_receta, analisisNutricional
import pandas as pd
from deep_translator import GoogleTranslator

def main():
    food = "pollo"
    alimento = "100 gr de " + food
    # Diccionario de mapeo de nombres en inglés (sin tilde) a nombres en español
    mapeo_nombres = {
        'Energia': 'Energia',
        'Lipidos totales (grasas)': 'Lipidos totales (grasas)',
        'Acidos grasos, saturados totales': 'Acidos grasos, saturados totales',
        'Acidos grasos, trans totales': 'Acidos grasos, trans totales',
        'Acidos grasos monoinsaturados totales': 'Acidos grasos monoinsaturados totales',
        'Acidos grasos poliinsaturados totales': 'Acidos grasos poliinsaturados totales',
        'Carbohidratos, por diferencia': 'Carbohidratos, por diferencia',
        'Fibra dietetica total': 'Fibra dietetica total',
        'Azucares, total incluyendo NLEA': 'Azucares, total incluyendo NLEA',
        'Proteina': 'Proteina',
        'Colesterol': 'Colesterol',
        'Sodio Na': 'Sodio Na',
        'Calcio': 'Calcio',
        'Magnesio, Mg': 'Magnesio, Mg',
        'Potasio, K': 'Potasio, K',
        'Hierro, Fe': 'Hierro, Fe',
        'Zinc, Zn': 'Zinc, Zn',
        'Fosforo, P': 'Fosforo, P',
        'Vitamina A, RAE': 'Vitamina A, RAE',
        'Vitamina C, acido ascorbico total': 'Vitamina C, acido ascorbico total',
        'Tiamina': 'Tiamina',
        'Riboflavina': 'Riboflavina',
        'Niacina': 'Niacina',
        'Vitamina B-6': 'Vitamina B-6',
        'Folato, DFE': 'Folato, DFE',
        'Folato, comida': 'Folato, comida',
        'Acido folico': 'Acido folico',
        'Vitamina B12': 'Vitamina B12',
        'Vitamina D (D2 + D3)': 'Vitamina D (D2 + D3)',
        'Vitamina E (alfa-tocoferol)': 'Vitamina E (alfa-tocoferol)',
        'Vitamina K (filoquinona)': 'Vitamina K (filoquinona)',
        'Agua': 'Agua'
    }


    print("Buscando receta para:", alimento)
    food = GoogleTranslator(source='auto', target='en').translate(alimento)
    analisis_data = analisisNutricional(food)
    analisis_data = pd.DataFrame(analisis_data)

    if not analisis_data.empty:
        # Mapear la primera columna (que contiene 'None')
        analisis_data.index = analisis_data.index.map(mapeo_nombres)
        print(analisis_data) 
    else:
        print("El DataFrame está vacío.")

if __name__ == "__main__":
    main()
