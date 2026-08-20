from django.urls import path
from . import views

urlpatterns = [
    path("", views.product_list, name="products"),

    path(
        "<int:pk>/",
        views.product_detail,
        name="product_detail"
    ),

    path(
        "add/",
        views.add_product,
        name="add_product"
    ),

    path(
        "edit/<int:pk>/",
        views.edit_product,
        name="edit_product"
    ),
    path(
    "delete/<int:pk>/",
    views.delete_product,
    name="delete_product",
),
path(
    "categories/",
    views.category_management,
    name="category_management"
),

path(
    "categories/<int:pk>/edit/",
    views.edit_category,
    name="edit_category"
),

path(
    "categories/<int:pk>/remove-image/",
    views.remove_category_image,
    name="remove_category_image"
),

path(
    "<int:pk>/review/",
    views.add_review,
    name="add_review",
),
]


