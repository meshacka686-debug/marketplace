from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Profile


class RegisterForm(UserCreationForm):

    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()

    role = forms.ChoiceField(
        choices=Profile.ROLE_CHOICES
    )

    phone = forms.CharField(max_length=20)

    address = forms.CharField(
        widget=forms.Textarea(attrs={"rows":3})
    )

    class Meta:
        model = User

        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
            "role",
            "phone",
            "address",
            "password1",
            "password2",
        )