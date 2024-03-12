from deep_translator import GoogleTranslator
import pandas as pd
from edamamApi import analisisNutricional

def traductor(texto, form):
    if form == 'es':
        return GoogleTranslator(source='auto', target='es').translate(text=texto)
    elif form == 'en':
        return GoogleTranslator(source='auto', target='en').translate(text=texto)

data = {
    "name": "Steak & chips salad",
    "image": "https://edamam-product-images.s3.amazonaws.com/web-img/4a2/4a2bc6e663b5fb8fcc91f425398ef0f0.jpg?X-Amz-Security-Token=IQoJb3JpZ2luX2VjEDoaCXVzLWVhc3QtMSJHMEUCIQDvO3Q%2Fa2BEoGpmr5y4m06sPBo4ED6xFbWONueJb4z70wIgJW%2BeoP7gR3XuelqDRTJ5VIwsCPW0UWiiHL0y8CEilrAquQUIQxAAGgwxODcwMTcxNTA5ODYiDMKvS4uROwg8nwvIuSqWBZVTcfCTN56CpquMnh6TH8UKZz1tj2mWMGSnYlpUzmG9rM561bsWiesoKGcr7T5riYeetd1rJ0PuvmkU6wnJOkvblOItdKm0gvLpZ6CKjQb9URdHOWqL9B%2FZgozhhj1U0B88%2FNJy3D1Dc5ws%2FxLBGR47EtMxwH8Ys%2B9GiVLVhjr5UxhPbuA10wjWEnpy4jQSU9DdxkKJ1nBD9I5GTdm3eaYbCPSDDmdc1JCQ1XsSt0EHNGjV%2Fobm0x8MbO3LroUE2%2BxFs86UU5V01Zn0Q4BXL1o7w5EFy%2Fz4m9VCgo786L%2B03gT2VtSkV8XVrbWytdpkJcNHRHTbOdjSn23Pu%2B5Xj0hboPyTuX5%2FIXO%2Feb%2FQZK46Rqfi8IzBtzB1nLTGxRp0weEos%2B2NUO8RIoIubvHWVvY3BqJiLZWBBy6E0C7c6t%2FcXmtPfy9olvjQx%2BCLlplSnwppfmexa9QUa9N6TyGdPhT%2BfVmj2ZM5Y7cgJH7i5%2FFv1q3eaS7hmMlDywiQow4lcA1BeYhffrLRIiT2pic0pnoiikceQ93xpnrrMmY7bEBxCcTptTO%2FzxbkemR85%2BTVVW2CTPquPxBHRdWWtseGHQ40cXk8BH7z1gSUpfk7ZgKMX0HDXpwoudIfM2F2xQVmVU2gx%2Bl%2BAKj66Sk12FlD2qzMYElez4vSbvgSGJQ3ISRB%2FD7RrJk%2FZTd54Gsy9vAtG0BUf3O6TTv8BXPZFgbLy%2BECQuJpcuxfRWEawjhMcZCwHvxczvR2NRy38p4ufYMxwVCF6uiH9Ad7%2BeWyS6VMGzokgO9nUoJIlk5X9FcrLPlmv19UtcEYbqgf2x69JyLKxP6QbysxpIbQTgpazLHdOi26z%2FinVVK%2Bbh8WNnLpUxoAtknBZQ9zMJO%2BwK8GOrEBqtTHFJPTECN7lqZ1DSlHcI12jwNF9D2VagAqk7drDCvAQhB%2Bckp%2FLiXEZPomgrHKCv1PjrDifs9iwPGnyiSW%2BM0N5MafEvSIINvYAazYAnjvOU%2FqO2C5ldjYZS%2BLhy%2Fv71MXxaFFzRrrnXzCFtg7KzySKWbzQIQY%2B3OuhecwIG8tlTO0jFDCiTBTN5Bbfzy0LX%2BFbDYAWOghkkQZVZhNLWg2UIEHR9QZysmm9r8Auufk&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20240312T101143Z&X-Amz-SignedHeaders=host&X-Amz-Expires=3600&X-Amz-Credential=ASIASXCYXIIFPZOST3VV%2F20240312%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=b21f3860a28c3217b6515dbf900a92edb64efdf4279d3afd62fdc10a2e0694e1",
    "recipe_link": "https://www.bbcgoodfood.com/recipes/steak-chips-salad",
    "diet_labels": "High-Fiber, Low-Sodium",
    "health_labels": "Sugar-Conscious, Dairy-Free, Gluten-Free, Wheat-Free, Egg-Free, Peanut-Free, Tree-Nut-Free, Soy-Free, Fish-Free, Shellfish-Free, Pork-Free, Crustacean-Free, Celery-Free, Sesame-Free, Lupine-Free, Mollusk-Free, Alcohol-Free",
    "ingredients": "['750g bag frozen potato wedges', '1 tbsp olive oil', '2 pieces sirloin steak , about 350g/12oz in total', '120g bag herb salad', '6 tbsp honey and mustard salad dressing , bought or homemade']"
}

columns_to_translate = ["name", "diet_labels", "health_labels", "ingredients"]

translated_data = {}
for col, val in data.items():
    if col in columns_to_translate:
        translated_data[col] = traductor(val, 'es')
    else:
        translated_data[col] = val

print(translated_data)
