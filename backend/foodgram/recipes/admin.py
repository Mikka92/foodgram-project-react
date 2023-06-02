from django.contrib import admin

from .models import (Favourit, Ingredient, IngredientForRecipe, Recipe,
                     ShoppingCart, Tag)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit',)
    search_fields = ('name', 'measurement_unit',)
    list_filter = ('name', 'measurement_unit',)


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug',)


class IngredientForRecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'ingredient', 'recipe', 'amount',)
    search_fields = ('recipe__name', 'ingredient__name',)
    list_editable = ('ingredient', 'amount',)
    list_filter = ('recipe__name',)


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'author', 'name', 'image', 'text',
        'cooking_time', 'date', 'favourites_count')
    search_fields = ('author__username', 'name', 'tags__name',)
    list_filter = ('author__username', 'name', 'tags__name',)

    def favourites_count(self, obj):
        return obj.favorites.count()


class FavouriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'user',)
    search_fields = ('recipe__name', 'user__username',)
    list_filter = ('recipe__name', 'user__username',)


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'user',)
    search_fields = ('recipe__name', 'user__username',)
    list_filter = ('recipe__name', 'user__username',)


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(IngredientForRecipe, IngredientForRecipeAdmin)
admin.site.register(Favourit, FavouriteAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
