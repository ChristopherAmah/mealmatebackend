from django.db import models


class Recipe(models.Model):
    meal_id = models.CharField(
        max_length=50, unique=True, help_text="Original ID from TheMealDB API"
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
