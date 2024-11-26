# hello/views.py

from django.shortcuts import render, get_object_or_404
from .models import Recipe
from .models import RecipeIngredient
from django.db.models import Q  # Import Q for complex queries
from django.core.paginator import Paginator
import re
import json

def parse_ingredient_groups(s):
    pattern = r'IngredientGroup\(ingredients=\[(.*?)\],\s*purpose=(\'(.*?)\'|None)\)'
    matches = re.findall(pattern, s, re.DOTALL)

    ingredient_groups = []

    for ingredients_str, _, purpose in matches:
        # Extract ingredients enclosed in single quotes
        ingredients = re.findall(r"'(.*?)'", ingredients_str)
        ingredient_groups.append({
            'purpose': purpose if purpose else None,
            'ingredients': ingredients
        })

    return ingredient_groups



def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    #recipe_ingredients = recipe.recipe_ingredients.all()
    # Initialize variables
    recipe_ingredients = RecipeIngredient.objects.filter(recipe=recipe)
    #ingredients_list = recipe.ingredient_groups.split('\n') if recipe.ingredient_groups else []
    instructions = recipe.instructions.split('\n') if recipe.instructions else []
    instructions_list = recipe.instructions.split('\n') if recipe.instructions else []
    equipment = recipe.equipment.split('\n') if hasattr(recipe, 'equipment') and recipe.equipment else []
    keywords = recipe.keywords.split(',') if hasattr(recipe, 'keywords') and recipe.keywords else []
    ingredients_list = parse_ingredient_groups(recipe.ingredient_groups)
    #ingredient_groups = recipe.ingredient_groups.split('\n') if recipe.ingredient_groups else []
    ingredient_groups = parse_ingredient_groups(recipe.ingredient_groups) if recipe.ingredient_groups else []

    context = {
        'recipe': recipe,
        'ingredients_list': ingredients_list,
        'ingredient_groups': ingredient_groups,
        'instructions': instructions,
        'equipment': equipment,
        'keywords': keywords,
        'instructions_list': instructions_list,
        'recipe_ingredients': recipe_ingredients,
    }
    return render(request, 'hello/recipe_detail.html', context)

def search(request):
    query = request.GET.get('q', '')
    recipes = []
    if query:
        recipes = Recipe.objects.filter(
            Q(title__icontains=query) |
            Q(ingredients__icontains=query) |
            Q(ingredient_groups__icontains=query)
        ).distinct()
    
    paginator = Paginator(recipes, 24)  # Show 24 recipes per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'recipes': page_obj,
        'query': query,
        'is_paginated': page_obj.has_other_pages(),
        'page_obj': page_obj,
    }
    return render(request, 'hello/search_results.html', context)

def index(request):
    query = request.GET.get('q', '')
    if query:
        recipes = Recipe.objects.filter(
            Q(title__icontains=query) |
            Q(ingredients__icontains=query) |
            Q(ingredient_groups__icontains=query)
        ).distinct()
        search = True
    else:
        recipes = Recipe.objects.all()
        search = False
    
    paginator = Paginator(recipes, 24)  # Show 24 recipes per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'recipes': page_obj,
        'query': query,
        'search': search,
    }
    return render(request, 'hello/index.html', context)


def recipe_list(request):
    recipe_list = Recipe.objects.all()  
    paginator = Paginator(recipe_list, 24)  # Show 24 recipes per page

    page_number = request.GET.get('page')
    recipes = paginator.get_page(page_number)

    return render(request, 'hello/index.html', {'recipes': recipes})

def metric_details(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    recipe_ingredients1 = recipe.recipe_ingredients.all()
    return render(request, 'hello/recipe_detail.html', {
        'recipe': recipe,
        'recipe_ingredients': recipe_ingredients1,
    })

def categories(request):
    return render(request, 'hello/categories.html')

def about(request):
    return render(request, 'hello/about.html')

def contact(request):
    return render(request, 'hello/contact.html')


