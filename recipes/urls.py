from django.urls import path
from . import views

urlpatterns = [
    path('recipes/', views.get_recipes, name='get_recipes'),
    # path("recipes/<int:meal_id>/", views.get_recipe_detail),
    path("recipes/<int:pk>/", views.get_recipe_detail, name="recipe-detail"),

]
