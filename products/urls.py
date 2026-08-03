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
]


