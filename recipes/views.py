from rest_framework.decorators import api_view
from rest_framework.response import Response
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


