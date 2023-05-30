from django.db.models.aggregates import Sum

from recipes.models import IngredientForRecipe


def get_shopping_cart(user):
    ingredients = IngredientForRecipe.objects.filter(
        recipe__shopping_cart__user=user
    ).values(
        'ingredient__name', 'ingredient__measurement_unit'
    ).annotate(
        total_amount=Sum('amount')
    )
    return [
        f'- {ing["ingredient__name"]}: '
        f'{ing["total_amount"]} '
        f'{ing["ingredient__measurement_unit"]}'
        for ing in ingredients
    ]
