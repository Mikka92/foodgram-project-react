from django.contrib import admin

from .models import (Favourit, Ingredient, IngredientForRecipe, Recipe,
                     ShoppingCart, Tag)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'measurement_unit',)
    search_fields = ('name', 'measurement_unit',)
    list_filter = ('name', 'measurement_unit',)


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


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('pk', 'recipe', 'user',)
    search_fields = ('recipe', 'user',)
    list_filter = ('recipe', 'user',)


admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(Tag)
admin.site.register(IngredientForRecipe)
admin.site.register(Favourit)
admin.site.register(ShoppingCart)
