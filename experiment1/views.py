from django.shortcuts import render, redirect
from admin_dashboard.models import ProductsModel
from django.shortcuts import render, redirect, get_object_or_404


def home_page(request):

    # =====================================================
    # NEW ARRIVALS
    # Latest products added to the store
    # =====================================================

    new_arrivals = ProductsModel.objects.filter(
        is_available=True,
        stock__gt=0
    ).order_by('-created_at')[:10]


    # =====================================================
    # FEATURED PRODUCTS
    # Products manually marked as featured
    # =====================================================

    featured_products = ProductsModel.objects.filter(
        is_available=True,
        is_featured=True,
        stock__gt=0
    ).order_by('-created_at')[:10]


    # =====================================================
    # CONTEXT
    # =====================================================

    context = {
        'new_arrivals': new_arrivals,
        'featured_products': featured_products,
    }


    return render(
        request,
        'customer/home.html',
        context
    )


def product_detail_page(request, slug):

    product = get_object_or_404(
        ProductsModel,
        slug=slug,
        is_available=True
    )

    sizes = product.sizes.all()

    has_stock = product.sizes.filter(
        is_available=True,
        stock__gt=0
    ).exists()

    context = {
        'product': product,
        'sizes': sizes,
        'has_stock': has_stock,
    }

    return render(
        request,
        'customer/product_detail.html',
        context
    )