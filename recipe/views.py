from django.shortcuts import render, HttpResponseRedirect, reverse
 
from recipe.models import Recipe, Author
from recipe.forms import AddRecipeForm, AddAuthorForm
# Create your views here.

def index_view(request):
    recipes = Recipe.objects.all()
    return render(request, "index.html", {"recipe": recipes, "welcome": "Welcome to Recipe World"})

def recipe_detail(request, recipe_id):
    recipes = Recipe.objects.filter(id=recipe_id).first()
    return render(request, "recipe.html", {"recipe": recipes})

# Got help from Matt Perry - this was for v1 recipebox assignment
def author_recipes(request, author_id):
    selected_author = Author.objects.filter(id=author_id).first()
    recipe_list = Recipe.objects.filter(author=selected_author)
    # breakpoint()
    return render(request, "author_recipes.html", {"recipes": recipe_list, "author": selected_author})


def recipe_form_view(request):
    if request.method == "POST":
        form = AddRecipeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Recipe.objects.create(
                title = data.get('title'),
                author = data.get('author'),
                description = data.get('description'),
                time_required = data.get('time_required'),
                instructions = data.get('instructions'),
            )
            return HttpResponseRedirect(reverse("homepage", args=[add_recipe.id]))
        
    form = AddRecipeForm()
    return render(request, "generic_form.html", {"form": form})


def author_form_view(request):
    if request.method =="POST":
       form =AddAuthorForm(request.POST)
       form.save()
       return HttpResponseRedirect(reverse("homepage", args=[add_author.id]))
        
    form = AddAuthorForm()
    return render(request, "generic_form.html", {"form": form})