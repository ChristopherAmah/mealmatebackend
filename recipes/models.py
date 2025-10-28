from django.db import models
from django.conf import settings


class Recipe(models.Model):
    """
    Stores recipe details fetched from TheMealDB or other external sources.
    """
    meal_id = models.CharField(
        max_length=50,
        unique=True,
        help_text="Original ID from TheMealDB API"
    )
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=100, blank=True, null=True)
    area = models.CharField(max_length=100, blank=True, null=True)
    instructions = models.TextField(blank=True, null=True)
    thumbnail = models.URLField(blank=True, null=True)
    tags = models.CharField(max_length=255, blank=True, null=True)
    youtube = models.URLField(blank=True, null=True)
    source = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Recipe"
        verbose_name_plural = "Recipes"

    def __str__(self):
        return self.title


class RecipeCategory(models.Model):
    """
    Allows users to assign custom categories to their recipes
    (e.g., 'Favorites', 'Vegan', 'Desserts', etc.).
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="recipe_categories"
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="user_categories"
    )
    category = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "recipe"],
                name="unique_user_recipe_category"
            )
        ]
        verbose_name = "Recipe Category"
        verbose_name_plural = "Recipe Categories"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} → {self.recipe.title} [{self.category}]"


class MealCalendar(models.Model):
    recipe_id = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=100, blank=True, null=True)
    thumbnail = models.URLField(blank=True, null=True)
    instructions = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.category})"