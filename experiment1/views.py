from django.shortcuts import render, redirect, get_object_or_404
from admin_dashboard.models import *
from .models import *

def home_page(request):

    home_page = HomePage.objects.first()

    if not home_page:
        home_page = HomePage.objects.create()

    hero_slides = home_page.hero_slides.filter(
        is_active=True
    ).order_by("display_order")


    new_arrivals = ProductsModel.objects.filter(
        is_available=True,
        stock__gt=0
    ).order_by("-created_at")[:10]

    featured_products = ProductsModel.objects.filter(
        is_available=True,
        is_featured=True,
        stock__gt=0
    ).order_by("-created_at")[:10]

    categories = Category.objects.all()

    context = {
        "home_page": home_page,
        "hero_slides": hero_slides,
        "new_arrivals": new_arrivals,
        "featured_products": featured_products,
        "categories": categories,
    }

    return render(
        request,
        "customer/home.html",
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



def about_page(request):
    """
    Display the published NAFI About Page.
    Content is managed from Django Admin.
    """

    about = (
        AboutPage.objects
        .filter(is_published=True)
        .prefetch_related(
            "values",
            "quality_items",
            "journey_items",
        )
        .first()
    )

    return render(
        request,
        "customer/about.html",
        {
            "about": about,
        },
    )


# =========================================================
# CONTACT PAGE
# =========================================================

from django.shortcuts import render

from admin_dashboard.models import (
    ContactPage,
    ContactService,
    ContactFAQ,
    ContactSocialLink,
)


def contact_page(request):

    contact = ContactPage.objects.filter(
        is_published=True
    ).first()


    # -----------------------------------------
    # CONTACT PAGE NOT AVAILABLE
    # -----------------------------------------

    if not contact:

        return render(
            request,
            "customer/contact.html",
            {
                "contact_page": None,
                "services": [],
                "faqs": [],
                "social_links": [],
                "sections": [],
            }
        )


    # -----------------------------------------
    # DYNAMIC SECTIONS
    # -----------------------------------------

    sections = []


    if contact.main_is_active:

        sections.append({
            "name": "main",
            "order": contact.main_order,
        })


    if contact.info_is_active:

        sections.append({
            "name": "info",
            "order": contact.info_order,
        })


    if contact.help_is_active:

        sections.append({
            "name": "help",
            "order": contact.help_order,
        })


    if contact.faq_is_active:

        sections.append({
            "name": "faq",
            "order": contact.faq_order,
        })


    if contact.social_is_active:

        sections.append({
            "name": "social",
            "order": contact.social_order,
        })


    if contact.final_is_active:

        sections.append({
            "name": "final",
            "order": contact.final_order,
        })


    sections.sort(
        key=lambda section: section["order"]
    )


    # -----------------------------------------
    # SERVICES
    # -----------------------------------------

    services = ContactService.objects.filter(
        contact_page=contact,
        is_active=True,
    ).order_by(
        "display_order",
        "id"
    )


    # -----------------------------------------
    # FAQ
    # -----------------------------------------

    faqs = ContactFAQ.objects.filter(
        contact_page=contact,
        is_active=True,
    ).order_by(
        "display_order",
        "id"
    )


    # -----------------------------------------
    # SOCIAL LINKS
    # -----------------------------------------

    social_links = ContactSocialLink.objects.filter(
        contact_page=contact,
        is_active=True,
    ).order_by(
        "display_order",
        "id"
    )


    # -----------------------------------------
    # CONTEXT
    # -----------------------------------------

    context = {

        "contact_page": contact,

        "services": services,

        "faqs": faqs,

        "social_links": social_links,

        "sections": sections,

    }


    return render(
        request,
        "customer/contact.html",
        context
    )


# =========================================================
# NAFI CART
# =========================================================


def add_to_cart(request, product_id):

    # -----------------------------------------------------
    # LOGIN REQUIRED
    # -----------------------------------------------------

    if not request.user.is_authenticated:
        return redirect("login")


    # -----------------------------------------------------
    # GET PRODUCT
    # -----------------------------------------------------

    product = get_object_or_404(
        ProductsModel,
        id=product_id,
        is_available=True
    )


    # -----------------------------------------------------
    # GET SIZE
    # -----------------------------------------------------

    size_id = request.POST.get("size_id")

    if not size_id:
        return redirect(
            "product_detail",
            slug=product.slug
        )


    # -----------------------------------------------------
    # GET PRODUCT SIZE
    # -----------------------------------------------------

    product_size = get_object_or_404(
        ProductSize,
        id=size_id,
        product=product,
        is_available=True
    )


    # -----------------------------------------------------
    # GET QUANTITY
    # -----------------------------------------------------

    try:
        quantity = int(
            request.POST.get("quantity", 1)
        )
    except (TypeError, ValueError):
        quantity = 1


    if quantity < 1:
        quantity = 1


    # -----------------------------------------------------
    # STOCK VALIDATION
    # -----------------------------------------------------

    if product_size.stock <= 0:
        return redirect(
            "product_detail",
            slug=product.slug
        )


    if quantity > product_size.stock:
        quantity = product_size.stock


    # -----------------------------------------------------
    # GET / CREATE CART
    # -----------------------------------------------------

    cart, created = Cart.objects.get_or_create(
        user=request.user
    )


    # -----------------------------------------------------
    # GET / CREATE CART ITEM
    # -----------------------------------------------------

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product_size=product_size,
        defaults={
            "quantity": quantity
        }
    )


    # -----------------------------------------------------
    # EXISTING ITEM
    # -----------------------------------------------------

    if not created:

        new_quantity = (
            cart_item.quantity + quantity
        )

        if new_quantity > product_size.stock:
            new_quantity = product_size.stock

        cart_item.quantity = new_quantity
        cart_item.save()


    # -----------------------------------------------------
    # REDIRECT CART
    # -----------------------------------------------------

    return redirect("cart_page")



# =========================================================
# CART PAGE
# =========================================================

def cart_page(request):

    if not request.user.is_authenticated:
        return redirect("login")


    # -----------------------------------------------------
    # GET / CREATE CART
    # -----------------------------------------------------

    cart, created = Cart.objects.get_or_create(
        user=request.user
    )


    # -----------------------------------------------------
    # CART ITEMS
    # -----------------------------------------------------

    cart_items = (
        cart.items
        .select_related(
            "product_size",
            "product_size__product"
        )
        .order_by("-created_at")
    )


    # -----------------------------------------------------
    # CONTEXT
    # -----------------------------------------------------

    context = {
        "cart": cart,
        "cart_items": cart_items,
    }


    return render(
        request,
        "customer/cart.html",
        context
    )



# =========================================================
# UPDATE CART
# =========================================================

def update_cart(request, item_id):

    if not request.user.is_authenticated:
        return redirect("login")


    # -----------------------------------------------------
    # GET CART
    # -----------------------------------------------------

    cart = get_object_or_404(
        Cart,
        user=request.user
    )


    # -----------------------------------------------------
    # GET CART ITEM
    # -----------------------------------------------------

    cart_item = get_object_or_404(
        CartItem,
        id=item_id,
        cart=cart
    )


    # -----------------------------------------------------
    # GET QUANTITY
    # -----------------------------------------------------

    try:
        quantity = int(
            request.POST.get("quantity", 1)
        )
    except (TypeError, ValueError):
        quantity = 1


    # -----------------------------------------------------
    # DELETE IF ZERO / NEGATIVE
    # -----------------------------------------------------

    if quantity <= 0:

        cart_item.delete()

        return redirect("cart_page")


    # -----------------------------------------------------
    # CURRENT PRODUCT SIZE
    # -----------------------------------------------------

    product_size = cart_item.product_size


    # -----------------------------------------------------
    # STOCK VALIDATION
    # -----------------------------------------------------

    if (
        not product_size.is_available
        or product_size.stock <= 0
    ):

        cart_item.delete()

        return redirect("cart_page")


    if quantity > product_size.stock:
        quantity = product_size.stock


    # -----------------------------------------------------
    # UPDATE
    # -----------------------------------------------------

    cart_item.quantity = quantity

    cart_item.save()


    return redirect("cart_page")



# =========================================================
# REMOVE CART ITEM
# =========================================================

def remove_from_cart(request, item_id):

    if not request.user.is_authenticated:
        return redirect("login")


    # -----------------------------------------------------
    # GET CART
    # -----------------------------------------------------

    cart = get_object_or_404(
        Cart,
        user=request.user
    )


    # -----------------------------------------------------
    # DELETE ITEM
    # -----------------------------------------------------

    cart_item = get_object_or_404(
        CartItem,
        id=item_id,
        cart=cart
    )

    cart_item.delete()


    return redirect("cart_page")



# =========================================================
# CLEAR CART
# =========================================================

def clear_cart(request):

    if not request.user.is_authenticated:
        return redirect("login")


    # -----------------------------------------------------
    # GET CART
    # -----------------------------------------------------

    cart = get_object_or_404(
        Cart,
        user=request.user
    )


    # -----------------------------------------------------
    # DELETE ALL ITEMS
    # -----------------------------------------------------

    cart.items.all().delete()


    return redirect("cart_page")



# =========================================================
# WISHLIST
# =========================================================

def add_to_wishlist(request, product_id):

    if not request.user.is_authenticated:
        return redirect("login")

    product = get_object_or_404(
        ProductsModel,
        id=product_id,
        is_available=True
    )

    wishlist, created = Wishlist.objects.get_or_create(
        user=request.user
    )

    wishlist_item, created = WishlistItem.objects.get_or_create(
        wishlist=wishlist,
        product=product
    )

    # If already exists, remove it
    if not created:
        wishlist_item.delete()

    return redirect(
        request.META.get(
            "HTTP_REFERER",
            "home_page"
        )
    )


def wishlist_page(request):

    if not request.user.is_authenticated:
        return redirect("login")

    wishlist, created = Wishlist.objects.get_or_create(
        user=request.user
    )

    wishlist_items = (
        wishlist.items
        .select_related("product")
        .order_by("-created_at")
    )

    context = {
        "wishlist": wishlist,
        "wishlist_items": wishlist_items,
    }

    return render(
        request,
        "customer/wishlist.html",
        context
    )

