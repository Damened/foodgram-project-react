from django.db.models import Sum
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from recipes.models import (Favorite, Ingredient, IngredientsAmount, Recipe,
                            ShoppingCart, Tag)
from users.models import Follow, User
from .filters import RecipeFilter, IngredientFilter
from .paginators import PageNumberPagination
from .permissions import AdminOrAuthor, AdminOrReadOnly
from .serializers import (FollowSerializer, IngredientSerializer,
                          RecipeCreateSerializer, RecipeFollowerSerializer,
                          RecipeSerializer, TagSerializer, UsersSerializer)


class UsersViewSet(UserViewSet):
    """Вьюсет для модели пользователей"""

    queryset = User.objects.all()
    serializer_class = UsersSerializer
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ("username", "email")
    permission_classes = (AllowAny,)

    def subscribed(self, request, id=None):
        follower = get_object_or_404(User, id=id)
        follow, _ = Follow.objects.get_or_create(
            user=request.user, author=follower
        )
        serializer = FollowSerializer(follow)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def unsubscribed(self, request, id=None):
        follower = get_object_or_404(User, id=id)
        Follow.objects.filter(user=request.user, author=follower).delete()
        return Response({"message": "Вы успешно отписаны"},
                        status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["post", "delete"],
            permission_classes=[permissions.IsAuthenticated])
    def subscribe(self, request, id):
        if request.method == "POST":
            return self.subscribed(request, id)
        return self.unsubscribed(request, id)

    @action(detail=False, methods=["get"],
            permission_classes=[permissions.IsAuthenticated])
    def subscriptions(self, request):
        following = request.user.follower.all()
        pages = self.paginate_queryset(following)
        serializer = FollowSerializer(pages, many=True)
        return self.get_paginated_response(serializer.data)


class TagViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели тегов"""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = (AdminOrReadOnly,)


class IngredientViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели ингредиентов"""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AdminOrReadOnly,)
    pagination_class = None
    filter_backends = (IngredientFilter,)
    search_fields = ("^name",)


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет для рецептов"""

    queryset = Recipe.objects.all()
    permission_classes = (AdminOrAuthor,)
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_queryset(self):
        recipes = Recipe.objects.prefetch_related(
            "ingredient_amount__ingredient", "tags").all()
        return recipes

    def get_serializer_class(self):
        if self.action == "list":
            return RecipeSerializer
        if self.action == "retrieve":
            return RecipeSerializer
        return RecipeCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        detail=True, methods=["post", "delete"],
        permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == "POST":
            Favorite.objects.create(user=request.user, recipe=recipe)
            serializer = RecipeFollowerSerializer(recipe)
            return Response(data=serializer.data,
                            status=status.HTTP_201_CREATED)
        deleted = get_object_or_404(Favorite, user=request.user,
                                    recipe=recipe)
        deleted.delete()
        return Response(
            {"message": "Рецепт успешно удален из избранного"},
            status=status.HTTP_204_NO_CONTENT,
        )

    @action(
        detail=True, methods=["post", "delete"],
        permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == "POST":
            ShoppingCart.objects.create(user=request.user, recipe=recipe)
            serializer = RecipeFollowerSerializer(recipe)
            return Response(data=serializer.data,
                            status=status.HTTP_201_CREATED)
        delete = get_object_or_404(ShoppingCart, user=request.user,
                                   recipe=recipe)
        delete.delete()
        return Response(
            {"message": "Рецепт успешно удален из покупок"},
            status=status.HTTP_204_NO_CONTENT,
        )

    def create_ingredients_file(self):
        """Метод для создания текстового файла списка покупок."""
        user = self.request.user
        ingredients = IngredientsAmount.objects.filter(
            recipe__shopping_cart__user=user
        ).order_by('ingredient__name').values(
            "ingredient__name", "ingredient__measurement_unit"
        ).annotate(amount=Sum("amount"))
        shopping_cart = []
        for ingredient in ingredients:
            shopping_cart.append(
                f'{ingredient["ingredient__name"]}'
                f'{ingredient["amount"]} '
                f'{ingredient["ingredient__measurement_unit"]}\n'
            )
        return shopping_cart

    @action(
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path=r"download_shopping_cart"
    )
    def download_shopping_cart(self, request, *args, **kwargs):
        content = self.create_ingredients_file()
        response = HttpResponse(content, content_type="text/plain")
        response["Content-Disposition"] = (
            'attachment; filename="ingredients.txt"'
        )
        return response
