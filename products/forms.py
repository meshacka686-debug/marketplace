from django import forms

from .models import Product, ProductReview


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product

        fields = [
            "category",
            "name",
            "description",
            "price",
            "quantity",
            "image",
            "available",
        ]

        widgets = {
            "category": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter product name"
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "Describe your product"
                }
            ),

            "price": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter price",
                    "step": "0.01"
                }
            ),

            "quantity": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter quantity",
                    "min": "1"
                }
            ),

            "image": forms.ClearableFileInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "available": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input"
                }
            ),
        }



class ProductReviewForm(forms.ModelForm):

    class Meta:
        model = ProductReview

        fields = [
            "rating",
            "comment",
        ]

        widgets = {

            "rating": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "comment": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "Tell other customers what you think about this product..."
                }
            ),
        }

        labels = {
            "rating": "Your Rating",
            "comment": "Your Comment",
        }