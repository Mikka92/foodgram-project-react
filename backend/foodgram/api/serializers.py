from djoser.serializers import UserCreateSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import PrimaryKeyRelatedField
from django.core.exceptions import ValidationError

from users.models import Subscription, User
from recipes.models import (Favourit, Ingredient, IngredientForRecipe, Recipe,
                            ShoppingCart, Tag)


class GetSubscription(metaclass=serializers.SerializerMetaclass):
    """Класс для получения информации о подписки на автора."""

    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        return user.is_authenticated and Subscription.objects.filter(
            user=user, author=obj).exists()


class CustomUserSerializer(UserCreateSerializer, GetSubscription):
    """Сериализатор для модели User."""

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
            'is_subscribed',
        )


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Tag."""

    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'color',
            'slug'
        )


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Ingredient."""

    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit'
        )


class IngredientForRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для добавлении ингридиента при создании рецепта."""

    id = PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all()
    )
    name = serializers.ReadOnlyField(
        source='ingredient.name'
    )
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientForRecipe
        fields = (
            'id',
            'amount',
            'name',
            'measurement_unit'
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['id'] = instance.ingredient.id
        return data


class RecipeReadSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Recipe чтение."""

    tags = TagSerializer(
        many=True,
        read_only=True
    )
    author = CustomUserSerializer(
        read_only=True
    )
    ingredients = IngredientForRecipeSerializer(
        source='ingredientrecipes',
        many=True
    )
    image = Base64ImageField()
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        return user.is_authenticated and Favourit.objects.filter(
            user=user, recipe=obj
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        return user.is_authenticated and ShoppingCart.objects.filter(
            user=user, recipe=obj
        ).exists()


class RecipeWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Recipe запись."""

    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    author = CustomUserSerializer(read_only=True)
    ingredients = IngredientForRecipeSerializer(
        many=True
    )
    image = Base64ImageField(required=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def validate_ingredient(self, value):
        if not value:
            raise ValidationError(
                'Нужно добавить ингридиент.'
            )
        if value['amount'] <= 0:
            raise ValidationError(
                'Количество должно быть больше 0!'
            )
        return value

    def validate_tags(self, value):
        if not value:
            raise ValidationError(
                'Нужно добавить тег!'
            )
        return value

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        ingredients_for_recipe = list(map(
            lambda ingredient: IngredientForRecipe(
                recipe=recipe,
                ingredient=ingredient.get('id'),
                amount=ingredient.get('amount')
            ),
            ingredients
        ))
        IngredientForRecipe.objects.bulk_create(
            ingredients_for_recipe
        )
        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', None)
        if tags:
            instance.tags.set(tags)
        ingredients = validated_data.pop('ingredients', None)
        if ingredients:
            instance.ingredients.clear()
            for ingredient in ingredients:
                amount = ingredient['amount']
                IngredientForRecipe.objects.update_or_create(
                    recipe=instance,
                    ingredient=ingredient.get('id'),
                    defaults={'amount': amount})
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        context = {'request': self.context.get('request')}
        return RecipeReadSerializer(instance, context=context).data


class RecipeShortSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Recipe короткий."""

    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )


class SubscriptionSerializer(serializers.ModelSerializer, GetSubscription):
    """Сериализатор информации о подписки пользователей."""

    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    def get_recipes(self, user):
        limit = self.context['request'].GET.get('recipes_limit')
        recipes = user.recipes.all()[
            :int(limit)
        ] if limit else user.recipes.all()
        return RecipeShortSerializer(recipes, many=True).data

    def validate_subscribe_yourself(self, value):
        if self.context['request'].user == self.context['author']:
            raise ValidationError('Нельзя подписаться на самого себя!')
        return value
