from edamamApi import buscar_receta, analisisNutricional
import pandas as pd
from deep_translator import GoogleTranslator

food = "pizza"
food = GoogleTranslator(source='auto', target='en').translate(food)
analisis_data = analisisNutricional(food)
if analisis_data is not None:
    analisis = pd.DataFrame(analisis_data)
    print(analisis)




