from django.urls import path
from . import views

urlpatterns = [
    path('recipes/', views.get_recipes, name='get_recipes'),
    # path("recipes/<int:meal_id>/", views.get_recipe_detail),
    path("recipes/<int:pk>/", views.get_recipe_detail, name="recipe-detail"),
    path('recipes/add-to-category/', views.add_to_category, name='recipe-add-to-category'),
    path("meal-calendar/", views.meal_calendar_view, name="meal-calendar"),
    path('meal-calendar/<int:pk>/', views.delete_meal_calendar, name='meal-calendar-delete'),
]
