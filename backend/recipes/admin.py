from django.contrib import admin

from .models import (Favorite, Ingredient, IngredientsAmount, Recipe,
                     ShoppingCart, Tag)


class OtherAdmin(admin.ModelAdmin):
    pass


class IngredientInRecipe(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 10
    min_num = 1


class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "measurement_unit",
    )
    list_filter = ("name",)


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "author",
    )
    list_filter = ("name", "author__username", "tags__name")
    inlines = (IngredientInRecipe,)


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "recipe",
    )
    list_filter = ("user",)


class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "recipe",
    )
    list_filter = ("user",)


admin.site.register(Tag, OtherAdmin)
admin.site.register(IngredientsAmount, OtherAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
admin.site.register(Favorite, FavoriteAdmin)
