from django.shortcuts import render, HttpResponseRedirect, reverse
# used this https://stackoverflow.com/questions/23557697/django-how-to-let-permissiondenied-exception-display-the-reason
#in reference on how to display an error to user if they don't have permission
from django.http import HttpResponseForbidden
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import FormView, TemplateView
from django.contrib.auth import get_user

from recipe.models import Recipe, Author, Favorite
from recipe.forms import AddRecipeForm, AddAuthorForm, LoginForm
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
    favorite_list = Favorite.objects.filter(user=selected_author)
    return render(request, "author_recipes.html", {"recipes": recipe_list,
                                                   "author": selected_author,
                                                   "favorites": favorite_list})


@login_required
def recipe_form_view(request):
    if request.method == "POST":
        form = AddRecipeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Recipe.objects.create(
                title = data.get('title'),
                author = request.user.author,
                description = data.get('description'),
                time_required = data.get('time_required'),
                instructions = data.get('instructions'),
            )
            return HttpResponseRedirect(reverse("homepage"))
        
    form = AddRecipeForm()
    return render(request, "generic_form.html", {"form": form})


@login_required
def author_form_view(request):
    if request.user.is_staff:
        if request.method =="POST":
            form =AddAuthorForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                new_user = User.objects.create_user(username=data.get("username"), password=data.get("password"))
                Author.objects.create(name=data.get("name"), user=new_user, bio=data.get("bio"))
            return HttpResponseRedirect(reverse("homepage"))
    else:
        return HttpResponseForbidden("You don't have permission to make an author")
        
    form = AddAuthorForm()
    return render(request, "generic_form.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data.get("username"), password=data.get("password"))
            if user:
                login(request, user)
                return HttpResponseRedirect(request.GET.get('next', reverse("homepage")))
    
    form = LoginForm()
    return render(request, "generic_form.html", {"form" : form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("homepage"))


@login_required
def edit_form_view(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    if request.method == "POST":
        form = AddRecipeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            recipe.title = data.get('title')
            recipe.description = data.get('description')
            recipe.time_required = data.get('time_required')
            recipe.instructions = data.get('instructions')
            recipe.author = recipe.author
            recipe.save()
            return HttpResponseRedirect(reverse("homepage"))
    else:
        form = AddRecipeForm(initial={
            'title': recipe.title,
            'description': recipe.description,
            'time_required': recipe.time_required,
            'instructions': recipe.instructions,
            'author': recipe.author
        })
        return render(request, "generic_form.html", {"form": form})

# TODO form can edit existing recipes that prepopulates with the information of the model being updated
# TODO logged in user can edit their recipes
# TODO admin user can edit all recipes
# TODO every user has a collection of favorite recipes
# TODO links to favorites viewable from author detail page
# TODO all recipes have a favorite button on them
# TODO favorite button is visible only logged in

def add_favorite(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    user = Author.objects.get(user=request.user)
    try:
        if Favorite.objects.filter(user=user).filter(recipe=recipe):
            return HttpResponseRedirect(reverse('homepage'))
    except LookupError:
        pass
    Favorite.objects.create(
        user=user,
        recipe=recipe)
    return HttpResponseRedirect(reverse('homepage'))



