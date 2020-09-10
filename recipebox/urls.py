"""recipebox URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from recipe import views

urlpatterns = [
    path('', views.index_view, name="homepage"),
    path('recipe/<int:recipe_id>/favorite/', views.add_favorite),
    path('recipe/<int:recipe_id>/edit/', views.edit_form_view),
    path('author/<int:author_id>/', views.author_recipes),
    path('recipe/<int:recipe_id>/', views.recipe_detail),
    path('addrecipe/', views.recipe_form_view, name="addrecipe"),
    path('addauthor/', views.author_form_view, name="addauthor"),
    path('login/', views.login_view, name="loginview"),
    path('logout/', views.logout_view, name="logout"),
    # path('signup/', views.signup_view, name="signup"),
    path('admin/', admin.site.urls),
]
