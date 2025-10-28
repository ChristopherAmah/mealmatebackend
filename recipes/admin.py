from django.contrib import admin
from .models import Recipe, RecipeCategory, MealCalendar


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """
    Admin configuration for Recipe model.
    """
    list_display = ("title", "category", "area", "created_at", "updated_at")
    list_filter = ("category", "area", "created_at")
    search_fields = ("title", "meal_id", "category", "tags")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")


@admin.register(RecipeCategory)
class RecipeCategoryAdmin(admin.ModelAdmin):
    """
    Admin configuration for RecipeCategory model.
    """
    list_display = ("user", "recipe", "category", "created_at")
    list_filter = ("category", "created_at")
    search_fields = ("user__username", "recipe__title", "category")
    autocomplete_fields = ("user", "recipe")
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)


from django.contrib import admin

@admin.register(MealCalendar)
class MealCalendarAdmin(admin.ModelAdmin):
    # Function to show shortened instructions
    def short_instructions(self, obj):
        if obj.instructions:
            return obj.instructions[:50] + "..." if len(obj.instructions) > 50 else obj.instructions
        return ""
    short_instructions.short_description = "Instructions"  # Column title in admin

    list_display = ('id', 'title', 'category', 'recipe_id', 'date_added', 'thumbnail', 'short_instructions')
    list_filter = ('category', 'date_added')
    search_fields = ('title', 'category', 'recipe_id')
    ordering = ('-date_added',)
    readonly_fields = ('date_added',)
