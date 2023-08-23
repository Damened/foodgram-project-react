from django_filters.rest_framework import (AllValuesMultipleFilter,
                                           BooleanFilter,
                                           FilterSet,
                                           ModelChoiceFilter)
from rest_framework.filters import SearchFilter
from recipes.models import Recipe, User


class RecipeFilter(FilterSet):
    """Фильтр рецептов."""
    tags = AllValuesMultipleFilter(field_name="tags__slug", label="tags")
    author = ModelChoiceFilter(queryset=User.objects.all())
    is_favorited = BooleanFilter(method='filter_is_favorited')
    is_in_shopping_cart = BooleanFilter(
        method='filter_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = ("author", "tags", "is_favorited", "is_in_shopping_cart")

    def filter_is_favorited(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            return queryset.filter(favorite__user=self.request.user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            return queryset.filter(shopping_cart__user=self.request.user)
        return queryset


class IngredientFilter(SearchFilter):
    """Фильтр для ингредиентов"""
    search_param = "name"
