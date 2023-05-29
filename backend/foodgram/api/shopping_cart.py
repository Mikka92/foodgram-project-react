from collections import defaultdict
from recipes.models import IngredientForRecipe


def get_shopping_cart(user):
    ingredients = IngredientForRecipe.objects.filter(
        recipe__shopping_cart__user=user
    )
    compressed_ingredients = defaultdict(int)
    for ing in ingredients:
        name = ing.ingredient.name
        measurement_unit = ing.ingredient.measurement_unit
        amount = ing.amount
        compressed_ingredients[(name, measurement_unit)] += amount
    return [
        f'- {name}: {amount} {measurement_unit}\n'
        for (name, measurement_unit), amount
        in compressed_ingredients.items()
    ]
