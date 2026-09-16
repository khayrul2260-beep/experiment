from admin_dashboard.models import Category
from .models import *

def navbar_categories(request):

    categories = Category.objects.filter(
        is_active=True
    ).order_by("created_at")

    return {
        "navbar_categories": categories
    }



def navbar_cart_count(request):

    cart_count = 0

    if request.user.is_authenticated:

        try:
            cart_count = request.user.cart.total_items
        except Cart.DoesNotExist:
            cart_count = 0

    return {
        "navbar_cart_count": cart_count
    }



def navbar_wishlist_count(request):

    wishlist_count = 0

    if request.user.is_authenticated:

        try:
            wishlist_count = request.user.wishlist.items.count()

        except Wishlist.DoesNotExist:
            wishlist_count = 0

    return {
        "navbar_wishlist_count": wishlist_count
    }


def wishlist_product_ids(request):

    product_ids = set()

    if request.user.is_authenticated:

        try:
            product_ids = set(
                request.user.wishlist.items.values_list(
                    "product_id",
                    flat=True
                )
            )

        except Wishlist.DoesNotExist:
            product_ids = set()

    return {
        "wishlist_product_ids": product_ids
    }

