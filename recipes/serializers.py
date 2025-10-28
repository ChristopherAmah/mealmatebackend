from rest_framework import serializers
from .models import Recipe, RecipeCategory, MealCalendar


class RecipeSerializer(serializers.ModelSerializer):
    """
    Serializes meal details fetched from external APIs or created manually.
    """
    class Meta:
        model = Recipe
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")


class RecipeCategorySerializer(serializers.ModelSerializer):
    """
    Serializes user recipe categories (e.g., Vegan, Keto).
    """
    recipe = RecipeSerializer(read_only=True)
    recipe_id = serializers.PrimaryKeyRelatedField(
        queryset=Recipe.objects.all(), source="recipe", write_only=True
    )

    class Meta:
        model = RecipeCategory
        fields = ["id", "user", "recipe", "recipe_id", "category", "created_at"]
        read_only_fields = ["id", "user", "created_at"]


class MealCalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = MealCalendar
        fields = "__all__"