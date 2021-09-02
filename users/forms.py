from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


# Create new forms that are created from Django UserCreationForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()


    # Model that is effected is the User model.
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2'
        ]