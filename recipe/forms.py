from django import forms
from recipe.models import Author, Recipe
    
    
class AddAuthorForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = Author
        fields = ["name", "bio"]
        

class AddRecipeForm(forms.Form):
    title = forms.CharField(max_length=50)
    description = forms.CharField(widget=forms.Textarea)
    # author = forms.ModelChoiceField(Author.objects.all())
    time_required = forms.CharField(max_length=20, widget=forms.Textarea)
    instructions = forms.CharField(widget=forms.Textarea)
    

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
