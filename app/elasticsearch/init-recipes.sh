#!/bin/bash

until $(curl --output /dev/null --silent --head --fail http://localhost:9200); do
    printf '.'
    sleep 1
done

curl -XPUT "http://localhost:9200/recetas" -H 'Content-Type: application/json' -d'
{
  "mappings": {
    "properties": {
      "name": { "type": "text" },
      "image": { "type": "keyword" },
      "recipe_link": { "type": "keyword" },
      "diet_labels": { "type": "keyword" },
      "health_labels": { "type": "keyword" },
      "ingredients": { "type": "text" }
    }
  }
}
'

# Agregar la receta inicial
curl -XPOST "http://localhost:9200/recetas/_doc/1" -H 'Content-Type: application/json' -d'
{
  "name": "Steak & chips salad",
  "image": "https://edamam-product-images.s3.amazonaws.com/web-img/4a2/4a2bc6e663b5fb8fcc91f425398ef0f0.jpg",
  "recipe_link": "https://www.bbcgoodfood.com/recipes/steak-chips-salad",
  "diet_labels": "High-Fiber, Low-Sodium",
  "health_labels": "Sugar-Conscious, Dairy-Free, Gluten-Free, Wheat-Free, Egg-Free, Peanut-Free, Tree-Nut-Free, Soy-Free, Fish-Free, Shellfish-Free, Pork-Free, Crustacean-Free, Celery-Free, Sesame-Free, Lupine-Free, Mollusk-Free, Alcohol-Free",
  "ingredients": ["750g bag frozen potato wedges", "1 tbsp olive oil", "2 pieces sirloin steak , about 350g/12oz in total", "120g bag herb salad", "6 tbsp honey and mustard salad dressing , bought or homemade"]
}
'
