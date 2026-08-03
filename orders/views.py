from uuid import uuid4
from django.shortcuts import get_object_or_404, redirect

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect

from cart.models import Cart
from .models import Order, OrderItem
@login_required
def confirm_order(request, pk):

    order = get_object_or_404(
        Order,
        pk=pk,
        user=request.user
    )

    if request.method == "POST":
        order.status = "completed"
        order.save()

        messages.success(
            request,
            "Order confirmed successfully."
        )

    return redirect("my_orders")

@login_required
def checkout(request):

    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    items = cart.items.select_related(
        "product"
    ).all()

    if not items.exists():
        messages.warning(
            request,
            "Your cart is empty."
        )
        return redirect("cart")

    if request.method == "POST":

        full_name = request.POST.get("full_name", "").strip()
        phone = request.POST.get("phone", "").strip()
        address = request.POST.get("address", "").strip()

        if not full_name or not phone or not address:
            messages.error(
                request,
                "Please complete all delivery information."
            )
            return render(
                request,
                "orders/checkout.html",
                {
                    "cart": cart,
                    "items": items,
                }
            )

        with transaction.atomic():

            order = Order.objects.create(
                user=request.user,
                order_number=f"ORD-{uuid4().hex[:10].upper()}",
                full_name=full_name,
                phone=phone,
                address=address,
                total_amount=cart.total_price,
            )

            for item in items:

                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    product_name=item.product.name,
                    price=item.product.price,
                    quantity=item.quantity,
                    subtotal=item.subtotal,
                )

            cart.items.all().delete()

        messages.success(
            request,
            "Your order has been placed successfully."
        )

        return redirect(
            "order_detail",
            order_number=order.order_number
        )

    return render(
        request,
        "orders/checkout.html",
        {
            "cart": cart,
            "items": items,
        }
    )


@login_required
def order_detail(request, order_number):

    order = Order.objects.get(
        order_number=order_number,
        user=request.user
    )

    return render(
        request,
        "orders/order_detail.html",
        {
            "order": order,
        }
    )


@login_required
def my_orders(request):

    orders = Order.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(
        request,
        "orders/my_orders.html",
        {
            "orders": orders,
        }
    )