from django.contrib import admin

from django.contrib import admin
from .models import Recipe, RecipeIngredient

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('recipe_id', 'title', 'total_time')

@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'type', 'qty', 'unit')
