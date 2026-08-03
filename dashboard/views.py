from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages



from cart.models import Cart
from orders.models import Order
from products.models import Product, Category
from accounts.models import Profile


def home(request):

    products = Product.objects.filter(
        available=True
    ).order_by("-created_at")

    categories = Category.objects.all()

    return render(
        request,
        "home.html",
        {
            "products": products,
            "categories": categories,
        }
    )


@login_required
def buyer_dashboard(request):

    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    orders = Order.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(
        request,
        "dashboard/buyer_dashboard.html",
        {
            "cart": cart,
            "orders": orders,
            "recent_orders": orders[:5],
            "total_orders": orders.count(),
        }
    )


@login_required
def seller_dashboard(request):

    if not hasattr(request.user, "profile"):
        return redirect("dashboard")

    if request.user.profile.role != "seller":
        return redirect("dashboard")

    products = Product.objects.filter(
        seller=request.user
    ).order_by("-created_at")

    return render(
        request,
        "dashboard/seller_dashboard.html",
        {
            "products": products,
            "total_products": products.count(),
        }
    )


@login_required
def profile(request):

    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":

        request.user.first_name = request.POST.get("first_name")
        request.user.last_name = request.POST.get("last_name")
        request.user.email = request.POST.get("email")
        request.user.save()

        profile.phone = request.POST.get("phone")
        profile.address = request.POST.get("address")

        if profile.role == "seller":
            profile.shop_name = request.POST.get("shop_name")
            profile.business_description = request.POST.get(
                "business_description"
            )

        if "profile_image" in request.FILES:
            profile.profile_image = request.FILES["profile_image"]

        profile.save()

        messages.success(
            request,
            "Profile updated successfully!"
        )

        return redirect("profile")

    return render(
        request,
        "dashboard/profile.html",
        {
            "profile": profile,
        }
    )