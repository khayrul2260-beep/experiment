from django.shortcuts import render, redirect
from admin_dashboard.models import *
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

    categories = Category.objects.all().order_by('created_at')

    # =====================================================
    # CONTEXT
    # =====================================================

    context = {
        'new_arrivals': new_arrivals,
        'featured_products': featured_products,
            'categories': categories,
    }


    return render(
        request,
        'customer/home.html',
        context
    )


def product_detail_page(request, slug):

    # ==================================================
    # GET PRODUCT
    # ==================================================

    product = get_object_or_404(
        ProductsModel,
        slug=slug,
        is_available=True
    )


    # ==================================================
    # GET PRODUCT SIZES
    # ==================================================

    sizes = product.sizes.all()


    # ==================================================
    # CHECK STOCK
    # ==================================================

    has_stock = product.sizes.filter(
        is_available=True,
        stock__gt=0
    ).exists()


    # ==================================================
    # GET PRODUCT IMAGES
    # ==================================================

    product_images = product.images.all().order_by(
        "sort_order",
        "created_at"
    )


    # ==================================================
    # SECONDARY IMAGE
    # ==================================================

    secondary_image = product_images.filter(
        image_type="secondary"
    ).first()


    # ==================================================
    # GALLERY IMAGES
    # ==================================================

    gallery_images = product_images.filter(
        image_type="gallery"
    )


    # ==================================================
    # CONTEXT
    # ==================================================

    context = {
        "product": product,
        "sizes": sizes,
        "has_stock": has_stock,

        # Main image
        "main_image": product.image,

        # Secondary image
        "secondary_image": secondary_image,

        # Gallery images
        "gallery_images": gallery_images,
    }


    # ==================================================
    # RENDER
    # ==================================================

    return render(
        request,
        "customer/product_detail.html",
        context
    )




def category_products_page(request, slug):

    # ==================================================
    # GET CATEGORY
    # ==================================================

    category = get_object_or_404(
        Category,
        slug=slug,
        is_active=True
    )


    # ==================================================
    # GET CATEGORY PRODUCTS
    # ==================================================

    products = category.products.filter(
        is_available=True,
        stock__gt=0
    ).order_by('-created_at')


    # ==================================================
    # CONTEXT
    # ==================================================

    context = {
        'category': category,
        'products': products,
    }


    # ==================================================
    # RENDER
    # ==================================================

    return render(
        request,
        'customer/category_products.html',
        context
    )

