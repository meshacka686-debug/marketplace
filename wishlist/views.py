from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Wishlist
from products.models import Product


@login_required
def add_to_wishlist(request, pk):

    product = get_object_or_404(Product, pk=pk)

    Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )

    return redirect(request.META.get("HTTP_REFERER", "/"))


@login_required
def my_wishlist(request):

    wishlist = Wishlist.objects.filter(
        user=request.user
    ).select_related("product")

    return render(
        request,
        "wishlist/my_wishlist.html",
        {
            "wishlist": wishlist
        }
    )


@login_required
def remove_wishlist(request, pk):

    item = get_object_or_404(
        Wishlist,
        id=pk,
        user=request.user
    )

    item.delete()

    return redirect("wishlist")