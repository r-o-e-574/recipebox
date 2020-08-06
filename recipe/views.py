from django.shortcuts import render

# Create your views here.
from recipe.models import Recipe, Author
# Create your views here.

def index_view(request):
    recipes = Recipe.objects.all()
    return render(request, "index.html", {"recipe": recipes, "welcome": "Welcome to Recipe World"})

def recipe_detail(request, recipe_id):
    recipes = Recipe.objects.filter(id=recipe_id).first()
    return render(request, "recipe.html", {"recipe": recipes})

# Got help from Matt Perry
def author_recipes(request, author_id):
    selected_author = Author.objects.filter(id=author_id).first()
    recipe_list = Recipe.objects.filter(author=selected_author)
    # breakpoint()
    return render(request, "author_recipes.html", {"recipes": recipe_list, "author": selected_author})