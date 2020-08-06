from django.contrib import admin

from recipe.models import Author, Recipe
# Register your models here.
admin.site.register(Author)
admin.site.register(Recipe)