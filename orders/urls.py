from django.urls import path

from . import views


urlpatterns = [

    # Checkout
    path(
        "checkout/",
        views.checkout,
        name="checkout"
    ),

    # Paystack callback
    path(
        "payment/callback/",
        views.payment_callback,
        name="payment_callback"
    ),

    # My orders
    path(
        "my-orders/",
        views.my_orders,
        name="my_orders"
    ),

    # Confirm order
    path(
        "confirm/<int:pk>/",
        views.confirm_order,
        name="confirm_order"
    ),

    # Order details
    path(
        "<str:order_number>/",
        views.order_detail,
        name="order_detail"
    ),
]