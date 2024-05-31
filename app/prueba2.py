from edamamApi import buscar_receta, analisisNutricional
import pandas as pd
from deep_translator import GoogleTranslator

def main():
    food = "100 gr costillas bbq"
    print("Buscando receta para:", food)
    food = GoogleTranslator(source='auto', target='en').translate(food)
    analisis_data = analisisNutricional(food)
    if analisis_data is not None:
        analisis = pd.DataFrame(analisis_data)
        if not analisis.empty:
            print(analisis)
        else:
            print("El DataFrame está vacío.")

if __name__ == "__main__":
    main()
