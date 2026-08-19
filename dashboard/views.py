from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Sum

from cart.models import Cart
from orders.models import Order, OrderItem
from products.models import Product, Category
from accounts.models import Profile


def home(request):

    products = Product.objects.filter(
        available=True
    ).select_related(
        "category",
        "seller"
    ).order_by("-created_at")

    categories = Category.objects.all()

    return render(
        request,
        "dashboard/home.html",
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

    # Make sure user has a profile
    if not hasattr(request.user, "profile"):
        return redirect("dashboard")

    # Only sellers can access this dashboard
    if request.user.profile.role != "seller":
        return redirect("dashboard")

    # Seller's products
    products = Product.objects.filter(
        seller=request.user
    ).order_by("-created_at")

    # --------------------------------------------------
    # SELLER ORDER ITEMS
    # --------------------------------------------------

    seller_items = OrderItem.objects.filter(
        product__seller=request.user
    ).select_related(
        "order",
        "product",
        "order__user",
    ).order_by(
        "-order__created_at"
    )

    # --------------------------------------------------
    # ORDERS CONTAINING THIS SELLER'S PRODUCTS
    # --------------------------------------------------

    seller_orders = Order.objects.filter(
        items__product__seller=request.user
    ).distinct().order_by(
        "-created_at"
    )

    # --------------------------------------------------
    # TOTAL ORDERS
    # --------------------------------------------------

    total_orders = seller_orders.count()

    # --------------------------------------------------
    # PAID SALES
    # --------------------------------------------------
    # Only count money from successfully paid orders.

    sales_result = seller_items.filter(
        order__payment_status="paid"
    ).aggregate(
        total=Sum("subtotal")
    )

    total_sales = sales_result["total"] or 0

    # --------------------------------------------------
    # PENDING ORDERS
    # --------------------------------------------------

    pending_orders = seller_orders.filter(
        status="pending"
    ).count()

    # --------------------------------------------------
    # PROCESSING ORDERS
    # --------------------------------------------------

    processing_orders = seller_orders.filter(
        status="processing"
    ).count()

    # --------------------------------------------------
    # COMPLETED ORDERS
    # --------------------------------------------------

    completed_orders = seller_orders.filter(
        status="completed"
    ).count()

    # --------------------------------------------------
    # RECENT ORDERS
    # --------------------------------------------------

    recent_orders = seller_orders[:10]

    return render(
        request,
        "dashboard/seller_dashboard.html",
        {
            "products": products,

            "total_products": products.count(),

            "seller_orders": seller_orders,

            "recent_orders": recent_orders,

            "total_orders": total_orders,

            "total_sales": total_sales,

            "pending_orders": pending_orders,

            "processing_orders": processing_orders,

            "completed_orders": completed_orders,
        }
    )


@login_required
def profile(request):

    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":

        request.user.first_name = request.POST.get(
            "first_name"
        )

        request.user.last_name = request.POST.get(
            "last_name"
        )

        request.user.email = request.POST.get(
            "email"
        )

        request.user.save()

        profile.phone = request.POST.get(
            "phone"
        )

        profile.address = request.POST.get(
            "address"
        )

        if profile.role == "seller":

            profile.shop_name = request.POST.get(
                "shop_name"
            )

            profile.business_description = request.POST.get(
                "business_description"
            )

        if "profile_image" in request.FILES:

            profile.profile_image = request.FILES[
                "profile_image"
            ]

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