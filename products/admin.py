from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "category",
        "seller",
        "price",
        "quantity",
        "available",
    )

    list_filter = (
        "category",
        "available",
    )

    search_fields = (
        "name",
        "description",
    )