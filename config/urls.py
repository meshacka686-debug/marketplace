from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    # Admin
    path("admin/", admin.site.urls),

    # Website
    path("", include("dashboard.urls")),

    # Accounts
    path("accounts/", include("accounts.urls")),

    # Products
    path("products/", include("products.urls")),

    # Cart
    path("cart/", include("cart.urls")),

    # Orders
    path("orders/", include("orders.urls")),

    # Wishlist
    path("wishlist/", include("wishlist.urls")),

    # API
    path("api/", include("api_app.urls")),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )