from django.contrib import admin

from .models import (Favourit, Ingredient, IngredientForRecipe, Recipe,
                     ShoppingList, Tag)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'unit_measurement',)
    search_fields = ('name', 'unit_measurement',)
    list_filter = ('name', 'unit_measurement',)


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug',)


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'author', 'name', 'image', 'description',
        'cooking_time', 'pub_date',)
    search_fields = ('author', 'name', 'tag',)
    list_filter = ('author', 'name', 'tag',)


class IngredientForRecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'ingredient', 'recipe', 'amount',)


class FavouritAdmin(admin.ModelAdmin):
    list_display = ('pk', 'recipe', 'user',)
    search_fields = ('recipe', 'user',)
    list_filter = ('recipe', 'user',)


class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ('pk', 'recipe', 'user',)
    search_fields = ('recipe', 'user',)
    list_filter = ('recipe', 'user',)


admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(Tag)
admin.site.register(IngredientForRecipe)
admin.site.register(Favourit)
admin.site.register(ShoppingList)
