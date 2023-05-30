from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import (SAFE_METHODS, AllowAny,
                                        IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from users.models import Subscription, User
from recipes.models import Favourit, Ingredient, Recipe, ShoppingCart, Tag
from .permissions import IsAuthorOrReadOnly
from .serializers import (CustomUserSerializer, IngredientSerializer,
                          RecipeReadSerializer, RecipeShortSerializer,
                          RecipeWriteSerializer, SubscriptionSerializer,
                          TagSerializer)
from .shopping_cart import get_shopping_cart
from .pagination import LimitPageNumberPagination
from .filters import NameSearchFilter, RecipeFilter


class CustomUserViewsSet(UserViewSet):
    """Вьюсет для работы с моделью User."""

    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = LimitPageNumberPagination
    permission_classes = (IsAuthenticatedOrReadOnly,)

    @action(
            detail=False,
            methods=['get'],
            permission_classes=[IsAuthenticated]
        )
    def subscriptions(self, request):
        user_subscriptions = User.objects.filter(
            subscribing__user=request.user
        )
        paginated_subscriptions = self.paginate_queryset(
            user_subscriptions
        )
        serialized_subscriptions = SubscriptionSerializer(
            paginated_subscriptions,
            many=True, context={'request': request}
        ).data
        return self.get_paginated_response(serialized_subscriptions)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated]
    )
    def subscribe(self, request, id):
        user = request.user
        author = get_object_or_404(User, id=id)

        if user == author:
            return Response(
                {'errors': 'Нельзя подписываться на самого себя!'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if request.method == 'POST':
            subscription, created = Subscription.objects.update_or_create(
                user=user, author=author
            )
            if not created:
                return Response(
                    {'errors': 'Вы уже подписаны на этого пользователя!'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer = SubscriptionSerializer(
                author,
                context={'request': request}
            )
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED)

        elif request.method == 'DELETE':
            user = request.user
            author = get_object_or_404(User, id=id)
            subscription = Subscription.objects.filter(
                user=user, author=author
            ).first()
            if subscription:
                subscription.delete()
                return Response(
                    {'message': 'Вы отписались от пользователя.'},
                    status=status.HTTP_204_NO_CONTENT,
                )

        return Response(
            {'errors': 'Некорректный запросc!'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )


class TagViewsSet(ReadOnlyModelViewSet):
    """Вьюсет для работы с моделью Tag."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = (AllowAny,)


class IngredientViewsSet(ReadOnlyModelViewSet):
    """Вьюсет для работы с моделью Ingredient."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    permission_classes = (AllowAny,)
    filter_backends = (NameSearchFilter,)
    search_fields = ('^name',)


class RecipeViewsSet(ModelViewSet):
    """Вьюсет для работы с моделью Recipe."""

    queryset = Recipe.objects.all()
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = LimitPageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    http_method_names = ['get', 'post', 'patch', 'create', 'delete']

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeReadSerializer
        return RecipeWriteSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)

    @action(
            detail=True,
            methods=['post', 'delete'],
            permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, pk=None):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)

        if request.method == 'POST':
            if Favourit.objects.filter(
                user=user, recipe=recipe
            ).exists():
                return Response(
                    {'errors': 'Рецепт уже есть в избранном!'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            Favourit.objects.create(
                user=user, recipe=recipe
            )
            serializer = RecipeShortSerializer(
                recipe, context={'request': request}
            )
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        elif request.method == 'DELETE':
            if not Favourit.objects.filter(
                user=user, recipe=recipe
            ).exists():
                return Response(
                    {'errors': 'Рецепта не добавлен в ибранное!'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            Favourit.objects.filter(
                user=user, recipe=recipe
            ).delete()
            return Response(
                {'message': 'Рецепт удален из избранного.'},
                status=status.HTTP_204_NO_CONTENT
            )

        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(
            detail=True,
            methods=['post', 'delete'],
            permission_classes=[IsAuthenticated]
        )
    def shopping_cart(self, request, pk=None):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)

        if request.method == 'POST':
            if ShoppingCart.objects.filter(
                user=user,
                recipe=recipe
            ).exists():
                return Response(
                    {'errors': 'Рецепт уже добавлен в список покупок!'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            ShoppingCart.objects.create(
                user=user,
                recipe=recipe
            )
            serializer = RecipeShortSerializer(
                recipe, context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        elif request.method == 'DELETE':
            if not ShoppingCart.objects.filter(
                user=user, recipe=recipe
            ).exists():
                return Response(
                    {'errors': 'Рецепт не добавлен в список покупок!'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            ShoppingCart.objects.filter(
                user=user, recipe=recipe
            ).delete()
            return Response(
                {'message': 'Рецепт удален из списка покупок.'},
                status=status.HTTP_204_NO_CONTENT
            )

        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(
        detail=False,
        methods=['get'],
        permission_classes=(IsAuthenticated,),
    )
    def download_shopping_cart(self, request):
        shopping_cart = get_shopping_cart(request.user)
        if not isinstance(shopping_cart, str):
            shopping_cart = '\n'.join(shopping_cart)
        filename = 'shopping-list.txt'
        response = HttpResponse(content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        response.write(shopping_cart)
        return response
