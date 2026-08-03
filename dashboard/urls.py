from django.urls import path
from . import views


urlpatterns = [

    # Marketplace homepage
    path(
        "",
        views.home,
        name="home"
    ),

    # Buyer dashboard
    path(
        "dashboard/",
        views.buyer_dashboard,
        name="dashboard"
    ),

    # Seller dashboard
    path(
        "seller/dashboard/",
        views.seller_dashboard,
        name="seller_dashboard"
    ),
    # User Profile
    path(
        "profile/",
        views.profile,
        name="profile"
    ),

]