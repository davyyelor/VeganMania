from edamamApi import buscar_receta, analisisNutricional
import pandas as pd
from deep_translator import GoogleTranslator

def main():
    food = "pollo"
    alimento = "100 gr de " + food


    print("Buscando receta para:", alimento)
    food = GoogleTranslator(source='auto', target='en').translate(alimento)
    analisis_data = analisisNutricional(food)
    analisis_data = pd.DataFrame(analisis_data)
    print(analisis_data)

if __name__ == "__main__":
    main()
