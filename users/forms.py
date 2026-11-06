"""Forms for the users app.

RegisterForm extends Django's built-in UserCreationForm (the standard,
battle-tested signup form) with an optional email field — so new students
can register themselves from the browser instead of an admin creating
accounts behind the scenes.
"""

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=False,
        help_text="Optional — useful later for password recovery.",
    )

    class Meta:
        model = User
        fields = ("username", "email")   # password1/password2 come from UserCreationForm
