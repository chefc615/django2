from django.test import TestCase

from hello.models import Recipe, RecipeIngredient

# Fetch a recipe
recipe = Recipe.objects.first()
print(recipe.title)

# Fetch ingredients for the recipe
ingredients = RecipeIngredient.objects.filter(recipe=recipe)
for ingredient in ingredients:
    print(ingredient)
