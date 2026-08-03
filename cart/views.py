from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import Cart, CartItem
from products.models import Product


def cart_view(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Please login to view your cart.")
        return redirect("login")

    cart, created = Cart.objects.get_or_create(user=request.user)

    return render(
        request,
        "cart/cart.html",
        {"cart": cart}
    )


def add_to_cart(request, product_id):
    if not request.user.is_authenticated:
        messages.warning(request, "Please login before adding products to your cart.")
        return redirect("login")

    product = get_object_or_404(
        Product,
        id=product_id,
        available=True
    )

    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if not created:
        if cart_item.quantity < product.quantity:
            cart_item.quantity += 1
            cart_item.save()
        else:
            messages.warning(request, "You cannot add more than the available stock.")
            return redirect("cart")

    messages.success(
        request,
        f"{product.name} was added to your cart."
    )

    return redirect("cart")


def remove_from_cart(request, item_id):
    if not request.user.is_authenticated:
        return redirect("login")

    item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user
    )

    item.delete()

    messages.success(request, "Product removed from your cart.")

    return redirect("cart")


def increase_quantity(request, item_id):
    if not request.user.is_authenticated:
        return redirect("login")

    item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user
    )

    if item.quantity < item.product.quantity:
        item.quantity += 1
        item.save()
    else:
        messages.warning(request, "You have reached the available stock.")

    return redirect("cart")


def decrease_quantity(request, item_id):
    if not request.user.is_authenticated:
        return redirect("login")

    item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user
    )

    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()

    return redirect("cart")