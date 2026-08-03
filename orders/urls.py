from django.urls import path

from . import views


urlpatterns = [

    path(
        "checkout/",
        views.checkout,
        name="checkout"
    ),

    path(
        "my-orders/",
        views.my_orders,
        name="my_orders"
    ),

    path(
        "<str:order_number>/",
        views.order_detail,
        name="order_detail"
    ),
    path(
    "confirm/<int:pk>/",
    views.confirm_order,
    name="confirm_order",
),

]