from edamamApi import EdamamApi

def main():
    analisis = EdamamApi()
    print(analisis.NutritionalAnalysis("apple"))
