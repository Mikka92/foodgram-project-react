from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import IngredientViewsSet, TagViewsSet, RecipeViewsSet, UserViewSet

router = DefaultRouter
router.register('ingredients', IngredientViewsSet, basename='ingredients')
router.register('tags', TagViewsSet, basename='tags')
router.register('resipes', RecipeViewsSet, basename='resipes')
router.register('users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
