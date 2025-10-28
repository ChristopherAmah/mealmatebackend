from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import RecipeCategory, MealCalendar
import requests

BASE_URL = "https://www.themealdb.com/api/json/v1/1"

@api_view(['GET'])
def get_recipes(request):
    """
    Fetch recipes from TheMealDB API and return them.
    """
    query = request.query_params.get('q', '')
    response = requests.get(f"{BASE_URL}/search.php", params={"s": query})
    
    # Handle invalid or missing results
    data = response.json()
    meals = data.get("meals") or []  # prevent NoneType errors

    recipes = []
    for meal in meals:
        recipes.append({
            "id": int(meal["idMeal"]),
            "name": meal["strMeal"],
            "note": meal.get("strInstructions", ""),
            "image": meal.get("strMealThumb", ""),
            "category": meal.get("strCategory", ""),
        })

    return Response(recipes)


# @api_view(['GET'])
# def get_recipe_detail(request, meal_id):
#     """Fetch a single recipe by ID from TheMealDB"""
#     response = requests.get(f"{BASE_URL}/lookup.php", params={"i": meal_id})
#     data = response.json()
#     meals = data.get("meals", [])

#     if not meals:
#         return Response({"detail": "Recipe not found"}, status=404)

#     meal = meals[0]
#     recipe_detail = {
#         "id": meal["idMeal"],
#         "title": meal["strMeal"],
#         "category": meal["strCategory"],
#         "area": meal["strArea"],
#         "instructions": meal["strInstructions"],
#         "thumbnail": meal["strMealThumb"],
#         "tags": meal.get("strTags"),
#         "youtube": meal.get("strYoutube"),
#         "source": meal.get("strSource"),
#     }

#     return Response(recipe_detail)



@api_view(['GET'])
def get_recipe_detail(request, pk):
    """
    Fetch a single recipe by ID from TheMealDB, including ingredients and measurements.
    """
    try:
        url = f"https://www.themealdb.com/api/json/v1/1/lookup.php?i={pk}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json().get("meals")

        if not data:
            return Response({"error": "Recipe not found"}, status=404)

        meal = data[0]

        # Extract ingredients and measurements
        ingredients = []
        for i in range(1, 21):  # TheMealDB provides up to 20 ingredients
            ingredient = meal.get(f"strIngredient{i}")
            measure = meal.get(f"strMeasure{i}")
            if ingredient and ingredient.strip():  # Skip empty ingredients
                ingredients.append({
                    "ingredient": ingredient.strip(),
                    "measure": measure.strip() if measure else ""
                })

        # Construct the recipe object
        recipe = {
            "id": meal.get("idMeal"),
            "title": meal.get("strMeal"),
            "category": meal.get("strCategory"),
            "area": meal.get("strArea"),
            "instructions": meal.get("strInstructions"),
            "thumbnail": meal.get("strMealThumb"),
            "tags": meal.get("strTags"),
            "youtube": meal.get("strYoutube"),
            "source": meal.get("strSource"),
            "ingredients": ingredients,
        }

        return Response(recipe)

    except requests.exceptions.RequestException as e:
        return Response({"error": f"Request failed: {str(e)}"}, status=500)
    except Exception as e:
        return Response({"error": f"Server error: {str(e)}"}, status=500)



from .models import Recipe, RecipeCategory, MealCalendar
from .serializers import RecipeSerializer, RecipeCategorySerializer, MealCalendarSerializer


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_to_category(request):
    """
    Adds a recipe to a selected category.
    If the recipe doesn't exist locally, fetch it from TheMealDB.
    """
    meal_id = request.data.get("meal_id")
    category_name = request.data.get("category")

    if not meal_id or not category_name:
        return Response(
            {"error": "meal_id and category are required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Try to get the recipe from local DB
    recipe = Recipe.objects.filter(meal_id=meal_id).first()

    if not recipe:
        # Fetch from TheMealDB if not found
        try:
            res = requests.get(f"https://www.themealdb.com/api/json/v1/1/lookup.php?i={meal_id}")
            res.raise_for_status()
            data = res.json().get("meals")

            if not data:
                return Response({"error": "Recipe not found on TheMealDB"}, status=404)

            meal = data[0]

            # Create new recipe record
            recipe = Recipe.objects.create(
                meal_id=meal.get("idMeal"),
                title=meal.get("strMeal"),
                category=meal.get("strCategory"),
                area=meal.get("strArea"),
                instructions=meal.get("strInstructions"),
                thumbnail=meal.get("strMealThumb"),
                tags=meal.get("strTags"),
                youtube=meal.get("strYoutube"),
                source=meal.get("strSource"),
            )

        except requests.exceptions.RequestException as e:
            return Response(
                {"error": f"Failed to fetch recipe details: {str(e)}"},
                status=500,
            )

    # Create or update recipe category
    recipe_category, created = RecipeCategory.objects.update_or_create(
        user=request.user,
        recipe=recipe,
        defaults={"category": category_name},
    )

    serializer = RecipeCategorySerializer(recipe_category)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "POST"])
def meal_calendar_view(request):
    if request.method == "GET":
        meals = MealCalendar.objects.all().order_by("-date_added")
        serializer = MealCalendarSerializer(meals, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = MealCalendarSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(["DELETE"])
def delete_meal_calendar(request, pk):
    try:
        meal = MealCalendar.objects.get(pk=pk)
        meal.delete()
        return Response({"message": "Meal deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    except MealCalendar.DoesNotExist:
        return Response({"error": "Meal not found"}, status=status.HTTP_404_NOT_FOUND)