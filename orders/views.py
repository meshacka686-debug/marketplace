from uuid import uuid4
from decimal import Decimal

import requests

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)
from django.urls import reverse
from django.utils import timezone

from cart.models import Cart

from .models import Order, OrderItem


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

        full_name = request.POST.get(
            "full_name",
            ""
        ).strip()

        phone = request.POST.get(
            "phone",
            ""
        ).strip()

        address = request.POST.get(
            "address",
            ""
        ).strip()

        # Check delivery information

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

        # Paystack requires customer email

        if not request.user.email:

            messages.error(
                request,
                "Please add an email address to your account before making payment."
            )

            return render(
                request,
                "orders/checkout.html",
                {
                    "cart": cart,
                    "items": items,
                }
            )

        # Get total

        total_amount = Decimal(
            str(cart.total_price)
        )

        # Generate unique order number

        order_number = (
            f"ORD-{uuid4().hex[:10].upper()}"
        )

        # Generate unique Paystack reference

        payment_reference = (
            f"PAY-{uuid4().hex}"
        )

        # Create order and order items

        with transaction.atomic():

            order = Order.objects.create(
                user=request.user,
                order_number=order_number,
                full_name=full_name,
                phone=phone,
                address=address,
                total_amount=total_amount,
                status="pending",
                payment_status="pending",
                payment_reference=payment_reference,
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

        # Convert Naira to Kobo

        amount_in_kobo = int(
            total_amount * 100
        )

        # Callback URL

        callback_url = request.build_absolute_uri(
            reverse("payment_callback")
        )

        # Paystack request

        payload = {
            "email": request.user.email,
            "amount": str(amount_in_kobo),
            "currency": "NGN",
            "reference": payment_reference,
            "channels": [
                "card"
            ],
            "callback_url": callback_url,
            "metadata": {
                "order_number": order.order_number,
                "user_id": request.user.id,
            },
        }

        headers = {
            "Authorization": (
                f"Bearer {settings.PAYSTACK_SECRET_KEY}"
            ),
            "Content-Type": "application/json",
        }

        try:

            response = requests.post(
                "https://api.paystack.co/transaction/initialize",
                json=payload,
                headers=headers,
                timeout=30,
            )

            data = response.json()

        except requests.RequestException:

            order.payment_status = "failed"

            order.save(
                update_fields=[
                    "payment_status",
                    "updated_at",
                ]
            )

            messages.error(
                request,
                "Unable to connect to the payment service. Please try again."
            )

            return redirect("checkout")

        # Payment initialized successfully

        if (
            response.status_code == 200
            and data.get("status")
            and data.get("data", {}).get(
                "authorization_url"
            )
        ):

            authorization_url = (
                data["data"]["authorization_url"]
            )

            return redirect(
                authorization_url
            )

        # Payment initialization failed

        order.payment_status = "failed"

        order.save(
            update_fields=[
                "payment_status",
                "updated_at",
            ]
        )

        messages.error(
            request,
            data.get(
                "message",
                "Payment could not be initialized."
            )
        )

        return redirect("checkout")

    return render(
        request,
        "orders/checkout.html",
        {
            "cart": cart,
            "items": items,
        }
    )


@login_required
def payment_callback(request):

    reference = request.GET.get(
        "reference"
    )

    if not reference:

        messages.error(
            request,
            "Payment reference was not provided."
        )

        return redirect("my_orders")

    order = get_object_or_404(
        Order,
        payment_reference=reference,
        user=request.user,
    )

    headers = {
        "Authorization": (
            f"Bearer {settings.PAYSTACK_SECRET_KEY}"
        ),
    }

    try:

        response = requests.get(
            (
                "https://api.paystack.co/"
                f"transaction/verify/{reference}"
            ),
            headers=headers,
            timeout=30,
        )

        data = response.json()

    except requests.RequestException:

        messages.error(
            request,
            "Unable to verify your payment."
        )

        return redirect(
            "order_detail",
            order_number=order.order_number
        )

    payment_data = data.get(
        "data",
        {}
    )

    transaction_status = payment_data.get(
        "status"
    )

    paid_amount = payment_data.get(
        "amount"
    )

    expected_amount = int(
        order.total_amount * 100
    )

    # Verify payment status AND amount

    if (
        data.get("status")
        and transaction_status == "success"
        and paid_amount == expected_amount
    ):

        # Prevent processing the same payment twice

        if order.payment_status != "paid":

            with transaction.atomic():

                order.payment_status = "paid"

                order.status = "processing"

                order.paid_at = timezone.now()

                order.save(
                    update_fields=[
                        "payment_status",
                        "status",
                        "paid_at",
                        "updated_at",
                    ]
                )

                # Empty cart only after successful payment

                cart = Cart.objects.filter(
                    user=order.user
                ).first()

                if cart:

                    cart.items.all().delete()

        messages.success(
            request,
            "Payment successful! Your order has been confirmed."
        )

    else:

        order.payment_status = "failed"

        order.save(
            update_fields=[
                "payment_status",
                "updated_at",
            ]
        )

        messages.error(
            request,
            "Payment was not successful."
        )

    return redirect(
        "order_detail",
        order_number=order.order_number
    )


@login_required
def order_detail(request, order_number):

    order = get_object_or_404(
        Order,
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


@login_required
def confirm_order(request, pk):

    order = get_object_or_404(
        Order,
        pk=pk,
        user=request.user
    )

    if order.payment_status != "paid":

        messages.error(
            request,
            "Please complete payment before confirming the order."
        )

        return redirect(
            "order_detail",
            order_number=order.order_number
        )

    order.status = "completed"

    order.save(
        update_fields=[
            "status",
            "updated_at",
        ]
    )

    messages.success(
        request,
        "Order confirmed successfully."
    )

    return redirect("my_orders")