from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from .models import Product, Category
from .forms import ProductForm


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
    product = get_object_or_404(Product, pk=pk)

    related_products = Product.objects.filter(
        category=product.category,
        available=True
    ).exclude(pk=product.pk)[:4]

    return render(
        request,
        "products/product_detail.html",
        {
            "product": product,
            "related_products": related_products,
        }
    )


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

            product = form.save(commit=False)
            product.seller = request.user
            product.save()

            messages.success(
                request,
                "Product added successfully!"
            )

            return redirect("seller_dashboard")

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

            product = form.save(commit=False)
            product.seller = request.user
            product.save()

            messages.success(
                request,
                "Product updated successfully!"
            )

            return redirect("seller_dashboard")

        messages.error(
            request,
            "Please correct the errors below."
        )

        print("=" * 60)
        print("FORM ERRORS:")
        print(form.errors)
        print("FILES:")
        print(request.FILES)
        print("=" * 60)

    else:

        form = ProductForm(instance=product)

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
            "Product deleted successfully!"
        )

        return redirect("seller_dashboard")

    return render(
        request,
        "products/delete_product.html",
        {
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

        return redirect("seller_dashboard")

    return render(
        request,
        "products/delete_product.html",
        {
            "product": product,
        }
    )