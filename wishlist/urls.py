from django.urls import path
from . import views

urlpatterns = [

    path(
        "",
        views.my_wishlist,
        name="wishlist"
    ),

    path(
        "add/<int:pk>/",
        views.add_to_wishlist,
        name="add_to_wishlist"
    ),

    path(
        "remove/<int:pk>/",
        views.remove_wishlist,
        name="remove_wishlist"
    ),

]