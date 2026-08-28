from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Profile


class RegisterForm(UserCreationForm):

    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "First name",
            }
        )
    )

    last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Last name",
            }
        )
    )

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Email address",
            }
        )
    )

    role = forms.ChoiceField(
        choices=Profile.ROLE_CHOICES,
        widget=forms.Select(
            attrs={
                "class": "form-select",
            }
        )
    )

    phone = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Phone number",
            }
        )
    )

    address = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Address",
                "rows": 3,
            }
        )
    )

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",
        ]

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields["username"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Username",
        })

        self.fields["password1"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Password",
        })

        self.fields["password2"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Confirm password",
        })


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = [
            "phone",
            "address",
            "profile_image",
            "shop_name",
            "business_description",
        ]

        widgets = {
            "phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Phone number",
                }
            ),

            "address": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Address",
                    "rows": 3,
                }
            ),

            "profile_image": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "shop_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Shop name",
                }
            ),

            "business_description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Describe your business",
                    "rows": 4,
                }
            ),
        }


class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
        ]

        widgets = {
            "username": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "first_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "last_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                }
            ),
        }