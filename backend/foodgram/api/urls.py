from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CustomUserViewsSet, IngredientViewsSet, RecipeViewsSet,
                    TagViewsSet)

app_name = 'api'
router = DefaultRouter()
router.register('users', CustomUserViewsSet, basename='users')
router.register('ingredients', IngredientViewsSet, basename='ingredients')
router.register('tags', TagViewsSet, basename='tags')
router.register('recipes', RecipeViewsSet, basename='recipes')

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
]
