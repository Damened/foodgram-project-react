from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from foodgram.settings import MIN_VALUE, MAX_VALUE
from users.models import User


class Tag(models.Model):
    """Модель для тегов"""

    name = models.CharField(
        verbose_name="Тег",
        max_length=200,
        unique=True,
    )
    color = models.CharField(
        verbose_name="Цвет",
        max_length=7,
        null=True,
    )
    slug = models.CharField(
        verbose_name="Slug",
        max_length=200,
        null=True,
        unique=True,
    )

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
        ordering = ("name",)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Модель для ингредиентов"""

    name = models.CharField(
        verbose_name="Ингридиент",
        max_length=200,
    )
    measurement_unit = models.CharField(
        verbose_name="Единица измерения",
        max_length=200,
    )

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"
        ordering = ("name",)

    def __str__(self):
        return f"{self.name} {self.measurement_unit}"


class Recipe(models.Model):
    """Модель рецептов"""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipes",
        verbose_name="Автор рецепта",
    )
    name = models.CharField(
        verbose_name="Название",
        max_length=200,
    )
    image = models.ImageField(
        verbose_name="Картинка",
    )
    text = models.TextField(
        verbose_name="Описание",
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name="Список ингредиентов",
        through="IngredientsAmount",
        related_name="recipes",
    )
    tags = models.ManyToManyField(
        Tag,
        related_name="recipes",
        verbose_name="Тег",
    )
    pub_date = models.DateTimeField(
        verbose_name="Дата публикации",
        auto_now_add=True,
    )
    cooking_time = models.PositiveSmallIntegerField(
        "Время приготовления (в минутах)",
        validators=[
            MinValueValidator(
                MIN_VALUE,
                message="Время приготовления должно быть больше 0"),
            MaxValueValidator(
                MAX_VALUE,
                message="Время приготовления должно быть не больше 32000")
        ],
    )

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"
        ordering = ("-pub_date",)

    def __str__(self):
        return self.name


class IngredientsAmount(models.Model):
    """Модель описывающая количество ингридиентов"""

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name="Рецепт",
        related_name="ingredient_amount",
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name="Ингредиент",
        related_name="ingredient_amount",
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name="Количество",
        validators=[
            MinValueValidator(
                MIN_VALUE,
                message="Количество ингредиентов должно быть больше 0"),
            MaxValueValidator(
                MAX_VALUE,
                message="Количество ингредиентов не должно быть больше 32000")
        ],
    )

    class Meta:
        verbose_name = "Количество ингридиент"
        verbose_name_plural = "Количество ингридиентов"
        ordering = ("ingredient",)

    def __str__(self):
        return f"{self.amount} {self.ingredient}"


class Favorite(models.Model):
    """Модель списка избранного"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="favorite",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name="Рецепт",
        related_name="favorite",
    )

    @classmethod
    def create(cls, user, recipe):
        item = cls(user=user, recipe=recipe)
        recipe.is_fovorited = True
        recipe.save()
        item.save
        return item


class ShoppingCart(models.Model):
    """Модель списка избранного"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="shopping_cart",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name="Рецепт",
        related_name="shopping_cart",
    )

    @classmethod
    def create(cls, user, recipe):
        item = cls(user=user, recipe=recipe)
        recipe.is_in_shopping_cart = True
        recipe.save()
        item.save
        return item
