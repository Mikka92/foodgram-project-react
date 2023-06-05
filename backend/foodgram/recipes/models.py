from django.conf import settings
from django.db import models
from django.db.models import UniqueConstraint

from users.models import User

from api.validators import (validate_cooking_time, validate_date,
                            validate_hex_color)


class Ingredient(models.Model):
    """"Модель ингредиент."""
    name = models.CharField(
        max_length=settings.LIMIT_NAME_LENGTH,
        verbose_name='Название'
    )
    measurement_unit = models.CharField(
        max_length=settings.LIMIT_MEASUREMENT_UNIT_LENGTH,
        verbose_name='Еденица измерения'
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Tag(models.Model):
    """"Модель тег."""
    name = models.CharField(
        max_length=settings.LIMIT_NAME_LENGTH,
        unique=True,
        verbose_name='Название'
    )
    color = models.CharField(
        max_length=settings.LIMIT_COLOR_LENGTH,
        validators=(validate_hex_color,),
        unique=True,
        verbose_name='Цвет HEX'
    )
    slug = models.SlugField(
        max_length=settings.LIMIT_SLUG_LENGTH,
        unique=True,
        verbose_name='Уникальный слаг'
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """"Модель рецепт."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    name = models.CharField(
        max_length=settings.LIMIT_NAME_LENGTH,
        verbose_name='Название'
    )
    image = models.ImageField(
        upload_to='recipe/',
        verbose_name='Изображение'
    )
    text = models.TextField(
        verbose_name='Описание'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name='recipes',
        verbose_name='Список ингредиентов',
        through='IngredientForRecipe'
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Тег'
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=(validate_cooking_time,),
        verbose_name='Время приготовления'
    )
    date = models.DateTimeField(
        auto_now_add=True,
        validators=(validate_date,),
        verbose_name='Дата публикации'
    )

    class Meta:
        ordering = ('-date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientForRecipe(models.Model):
    """"Модель ингредиенты для рецепта."""
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredientrecipes',
        verbose_name='Ингредиент'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredientrecipes',
        verbose_name='Рецепт'
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Колличество'
    )

    class Meta:
        verbose_name = 'Ингредиенты для рецепта'
        verbose_name_plural = 'Ингредиенты для рецепта'

    def __str__(self):
        return f'{self.ingredient.name} - {self.amount}'


class Favourit(models.Model):
    """"Модель для избранных рецепотв."""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь'
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'

    def __str__(self):
        return f'{self.user} liked {self.recipe}'


class ShoppingCart(models.Model):
    """Модель для списка покупок."""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping',
        verbose_name='Рецепт'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping',
        verbose_name='Пользователь'
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Список покупок'
        constraints = (
            UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_shopping_cart'
            ),
        )

    def __str__(self):
        return f'{self.recipe} in {self.user} cart'
