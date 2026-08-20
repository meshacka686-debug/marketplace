from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db import models
from django.db.models import Avg
from .models import Product, Category, ProductReview
from .forms import ProductForm, ProductReviewForm

def product_list(request):

    products = Product.objects.filter(
        available=True
    )

    categories = Category.objects.all()

    category_id = request.GET.get("category")

    if category_id:
        products = products.filter(
            category_id=category_id
        )

    return render(
        request,
        "products/product_list.html",
        {
            "products": products,
            "categories": categories,
        }
    )


def product_detail(request, pk):

    product = get_object_or_404(
        Product.objects.select_related(
            "category",
            "seller"
        ),
        pk=pk
    )

    reviews = product.reviews.select_related(
        "user"
    ).all()

    average_rating = reviews.aggregate(
        average=Avg("rating")
    )["average"]

    related_products = Product.objects.filter(
        category=product.category,
        available=True
    ).exclude(
        pk=product.pk
    )[:4]

    return render(
        request,
        "products/product_detail.html",
        {
            "product": product,
            "reviews": reviews,
            "average_rating": average_rating,
            "related_products": related_products,
        }
    )
@login_required
def add_review(request, pk):

    product = get_object_or_404(
        Product,
        pk=pk
    )

    # Check if this user already reviewed this product
    existing_review = ProductReview.objects.filter(
        product=product,
        user=request.user
    ).first()

    if existing_review:
        messages.warning(
            request,
            "You have already reviewed this product."
        )

        return redirect(
            "product_detail",
            pk=product.pk
        )

    if request.method == "POST":

        form = ProductReviewForm(
            request.POST
        )

        if form.is_valid():

            review = form.save(
                commit=False
            )

            review.product = product
            review.user = request.user

            review.save()

            messages.success(
                request,
                "Thank you! Your review has been added."
            )

            return redirect(
                "product_detail",
                pk=product.pk
            )

    else:

        form = ProductReviewForm()

    return render(
        request,
        "products/add_review.html",
        {
            "form": form,
            "product": product,
        }
    )

# ==================================================
# PRODUCT MANAGEMENT
# ==================================================

@login_required
def add_product(request):

    if not hasattr(request.user, "profile"):
        return redirect("dashboard")

    if request.user.profile.role != "seller":
        return redirect("dashboard")

    if request.method == "POST":

        form = ProductForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            product = form.save(
                commit=False
            )

            product.seller = request.user
            product.save()

            messages.success(
                request,
                "Product added successfully!"
            )

            return redirect(
                "seller_dashboard"
            )

        messages.error(
            request,
            "Please correct the errors below."
        )

    else:

        form = ProductForm()

    return render(
        request,
        "products/add_product.html",
        {
            "form": form,
        }
    )


@login_required
def edit_product(request, pk):

    product = get_object_or_404(
        Product,
        pk=pk,
        seller=request.user
    )

    if request.method == "POST":

        form = ProductForm(
            request.POST,
            request.FILES,
            instance=product
        )

        if form.is_valid():

            product = form.save(
                commit=False
            )

            product.seller = request.user
            product.save()

            messages.success(
                request,
                "Product updated successfully!"
            )

            return redirect(
                "seller_dashboard"
            )

        messages.error(
            request,
            "Please correct the errors below."
        )

    else:

        form = ProductForm(
            instance=product
        )

    return render(
        request,
        "products/edit_product.html",
        {
            "form": form,
            "product": product,
        }
    )


@login_required
def delete_product(request, pk):

    product = get_object_or_404(
        Product,
        pk=pk,
        seller=request.user
    )

    if request.method == "POST":

        product.delete()

        messages.success(
            request,
            "Product deleted successfully."
        )

        return redirect(
            "seller_dashboard"
        )

    return render(
        request,
        "products/delete_product.html",
        {
            "product": product,
        }
    )


# ==================================================
# CATEGORY MANAGEMENT
# ==================================================

@login_required
def category_management(request):

    categories = Category.objects.all().order_by(
        "name"
    )

    return render(
        request,
        "products/category_management.html",
        {
            "categories": categories,
        }
    )


@login_required
def edit_category(request, pk):

    category = get_object_or_404(
        Category,
        pk=pk
    )

    if request.method == "POST":

        name = request.POST.get(
            "name",
            ""
        ).strip()

        image = request.FILES.get(
            "image"
        )

        if name:
            category.name = name

        if image:
            # Delete old Cloudinary image
            if category.image:
                category.image.delete(
                    save=False
                )

            category.image = image

        category.save()

        messages.success(
            request,
            f"{category.name} updated successfully."
        )

        return redirect(
            "category_management"
        )

    return render(
        request,
        "products/edit_category.html",
        {
            "category": category,
        }
    )


@login_required
def remove_category_image(request, pk):

    category = get_object_or_404(
        Category,
        pk=pk
    )

    if request.method == "POST":

        if category.image:

            category.image.delete(
                save=False
            )

            category.image = None
            category.save(
                update_fields=["image"]
            )

        messages.success(
            request,
            f"Image removed from {category.name}."
        )

    return redirect(
        "category_management"
    )