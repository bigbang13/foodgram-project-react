from django.core.validators import MinValueValidator
from django.db import models
from users.models import User

MINCOOKINGTIME = 1
MINAMOUNT = 1


class Ingredient(models.Model):
    name = models.CharField(
        "Ингредиент",
        max_length=256
    )
    measurement_unit = models.CharField(
        "Единица измерения",
        max_length=256
    )

    class Meta:
        ordering = ("name",)
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"

    def __str__(self) -> str:
        return self.name


class Tag(models.Model):
    name = models.CharField(
        "Название",
        max_length=200
    )
    color = models.CharField(
        "Цвет",
        max_length=7
    )
    slug = models.SlugField(
        "Ссылка",
        max_length=200,
        unique=True
    )

    class Meta:
        ordering = ("-id",)
        verbose_name = "Тэг"
        verbose_name_plural = "Тэги"

    def __str__(self) -> str:
        return self.name


class Recipe(models.Model):
    name = models.CharField(
        "Название рецепта",
        max_length=256
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name="recipes",
        through="RecipeIngredient"
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name="Тэги",
        related_name="recipes"
    )
    image = models.ImageField(
        "Изображение",
        upload_to="",
        blank=True,
        null=True
    )
    text = models.TextField(
        "Описание рецепта"
    )
    cooking_time = models.IntegerField(
        verbose_name="Время приготовления (минуты)",
        validators=[
            MinValueValidator(
                MINCOOKINGTIME,
                message="Время не может быть меньше {MINCOOKINGTIME} мин."
            ),
        ]
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор",
        related_name="recipes"
    )
    pub_date = models.DateTimeField(
        "Дата публикации",
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ("-pub_date",)
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"

    def get_tags(self):
        return "\n".join([t.tags for t in self.tags.all()])

    def get_ingredients(self):
        return "\n".join([i.ingredients for i in self.ingredients.all()])

    def __str__(self) -> str:
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name="Рецепт",
        related_name="ingrrecipes"
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name="Ингредиент",
        related_name="ingrrecipes"
    )
    amount = models.PositiveIntegerField(
        verbose_name="Количество",
        validators=[
            MinValueValidator(
                MINAMOUNT,
                message="Количество не может быть меньше {MINAMOUNT}"
            ),
        ]
    )

    class Meta:
        ordering = ("-id",)
        verbose_name = "Количество ингредиента"
        verbose_name_plural = "Количество ингредиентов"
        constraints = [
            models.UniqueConstraint(
                fields=("recipe", "ingredient",),
                name="unique ingredient"
            )
        ]

    def __str__(self):
        return f'{self.ingredient}, {self.amount}'


class FavoriteRecipes(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='favorite'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='favorite'
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='add_favorite'
            ),
        ]


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='shopping_cart'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='shopping_cart'
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Список покупок'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='add_shopping_cart'
            ),
        ]
