from django.conf import settings
from django.db import models
from users.models import User


class Ingredient(models.Model):
    """"Модель ингредиент"""
    name = models.CharField(
        max_length=settings.LIMIT_NAME_LENGHT,
        verbose_name='Название'
    )
    measurement_unit = models.CharField(
        max_length=settings.LIMIT_MU_LENGHT,
        verbose_name='Еденица измерения'
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Tag(models.Model):
    """"Модель тег"""
    name = models.CharField(
        max_length=settings.LIMIT_NAME_LENGHT,
        verbose_name='Название'
    )
    color = models.CharField(
        max_length=settings.LIMIT_COLOR_LENGHT,
        unique=True,
        verbose_name='Цвет HEX'
    )
    slug = models.SlugField(
        max_length=settings.LIMIT_SLUG_LENGHT,
        unique=True,
        verbose_name='Уникальный слаг'
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """"Модель рецепт"""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    name = models.CharField(
        max_length=settings.LIMIT_NAME_LENGHT,
        verbose_name='Название'
    )
    image = models.ImageField(
        upload_to='recipe/',
        verbose_name='Изображение'
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name='recipes',
        verbose_name='Список ингредиентов'
    )
    tag = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Тег'
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления'
    )
    pub_date = models.DateField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientForRecipe(models.Model):
    """"Модель ингредиенты для рецепта"""
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Колличество'
    )

    class Meta:
        verbose_name = 'Ингредиенты для рецепта'
        verbose_name_plural = 'Ингредиенты для рецепта'

    def __str__(self):
        return self.name


class Favourit(models.Model):
    """"Модель для избранных рецепотв"""
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
        return self.name


class ShoppingCart(models.Model):
    """Модель для списка покупок"""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Рецепт'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Пользователь'
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Список покупок'

    def __str__(self):
        return self.name
