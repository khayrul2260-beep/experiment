from django.shortcuts import render, redirect, get_object_or_404
from admin_dashboard.models import *
from .models import *
from django.http import JsonResponse
from types import SimpleNamespace


# =========================================================
# GUEST CART HELPERS
# =========================================================

def _get_guest_cart(request):

    return request.session.get(
        "guest_cart",
        {}
    )


def _save_guest_cart(request, guest_cart):

    request.session["guest_cart"] = guest_cart

    request.session.modified = True


def _clear_guest_cart(request):

    request.session.pop(
        "guest_cart",
        None
    )

    request.session.modified = True



# =========================================================
# BUILD GUEST CART ITEMS
# =========================================================

def _get_guest_cart_items(request):

    guest_cart = _get_guest_cart(request)

    cart_items = []

    valid_cart = {}

    for cart_key, data in guest_cart.items():

        product = ProductsModel.objects.filter(
            id=data.get("product_id"),
            is_available=True
        ).first()

        if not product:
            continue


        product_size = ProductSize.objects.filter(
            id=data.get("size_id"),
            product=product,
            is_available=True,
            stock__gt=0
        ).first()

        if not product_size:
            continue


        quantity = int(
            data.get(
                "quantity",
                1
            )
        )


        if quantity > product_size.stock:

            quantity = product_size.stock


        if quantity < 1:
            continue


        valid_cart[cart_key] = {

            "product_id": product.id,

            "size_id": product_size.id,

            "quantity": quantity,

        }


        unit_price = (
            product.discount_price
            if product.discount_price
            else product.price
        )


        total_price = (
            unit_price *
            quantity
        )


        cart_item = SimpleNamespace(

            key=cart_key,

            product=product,

            product_size=product_size,

            size=product_size.size,

            quantity=quantity,

            unit_price=unit_price,

            total_price=total_price,

        )


        cart_items.append(
            cart_item
        )


    # Remove invalid/out-of-stock items
    _save_guest_cart(
        request,
        valid_cart
    )


    return cart_items


# =========================================================
# GUEST CART SUMMARY
# =========================================================

def _get_guest_cart_summary(cart_items):

    total_items = sum(
        item.quantity
        for item in cart_items
    )


    subtotal = sum(
        item.total_price
        for item in cart_items
    )


    return SimpleNamespace(

        total_items=total_items,

        subtotal=subtotal,

    )


# =========================================================
# HOME MAIN
# =========================================================    



def home_page(request):

    home_page = HomePage.objects.first()

    if not home_page:
        home_page = HomePage.objects.create()

    hero_slides = home_page.hero_slides.filter(
        is_active=True
    ).order_by("display_order")

    new_arrivals = ProductsModel.objects.filter(
        is_available=True,
    ).order_by("-created_at")[:15]
    
    for product in new_arrivals:
        product.is_out_of_stock = not product.sizes.filter(
            is_available=True,
            stock__gt=0
        ).exists()
    
    
    all_products = ProductsModel.objects.filter(
        is_available=True
    ).order_by("-created_at")[:15]
    
    for product in all_products:
        product.is_out_of_stock = not product.sizes.filter(
            is_available=True,
            stock__gt=0
        ).exists()

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
        "all_products": all_products,
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
# GUEST UPDATE CART
# =========================================================

def guest_update_cart(request, item_key):

    guest_cart = _get_guest_cart(request)


    if item_key not in guest_cart:

        return redirect("cart_page")


    data = guest_cart[item_key]


    product = ProductsModel.objects.filter(
        id=data.get("product_id"),
        is_available=True
    ).first()


    if not product:

        guest_cart.pop(
            item_key,
            None
        )

        _save_guest_cart(
            request,
            guest_cart
        )

        return redirect("cart_page")


    product_size = ProductSize.objects.filter(
        id=data.get("size_id"),
        product=product,
        is_available=True
    ).first()


    if not product_size:

        guest_cart.pop(
            item_key,
            None
        )

        _save_guest_cart(
            request,
            guest_cart
        )

        return redirect("cart_page")


    try:

        quantity = int(
            request.POST.get(
                "quantity",
                1
            )
        )

    except (TypeError, ValueError):

        quantity = 1


    if quantity <= 0:

        guest_cart.pop(
            item_key,
            None
        )

    else:

        if quantity > product_size.stock:

            quantity = product_size.stock


        guest_cart[item_key]["quantity"] = (
            quantity
        )


    _save_guest_cart(
        request,
        guest_cart
    )


    return redirect("cart_page")

# =========================================================
# GUEST REMOVE
# =========================================================

def guest_remove_from_cart(request, item_key):

    guest_cart = _get_guest_cart(request)


    guest_cart.pop(
        item_key,
        None
    )


    _save_guest_cart(
        request,
        guest_cart
    )


    return redirect("cart_page")

# =========================================================
# GUEST REMOVE
# =========================================================

def guest_remove_from_cart(request, item_key):

    guest_cart = _get_guest_cart(request)


    guest_cart.pop(
        item_key,
        None
    )


    _save_guest_cart(
        request,
        guest_cart
    )


    return redirect("cart_page")

def clear_cart(request):

    if request.user.is_authenticated:

        cart = get_object_or_404(
            Cart,
            user=request.user
        )

        cart.items.all().delete()

        return redirect("cart_page")


    # Guest
    _clear_guest_cart(request)

    return redirect("cart_page")

def guest_add_another_size(request, item_key):

    guest_cart = _get_guest_cart(request)

    if item_key not in guest_cart:
        return redirect("cart_page")

    data = guest_cart[item_key]

    product = ProductsModel.objects.filter(
        id=data.get("product_id"),
        is_available=True
    ).first()

    if not product:
        return redirect("cart_page")

    size_id = request.POST.get("size_id")

    if not size_id:
        return redirect("cart_page")

    product_size = ProductSize.objects.filter(
        id=size_id,
        product=product,
        is_available=True
    ).first()

    if not product_size:
        return redirect("cart_page")

    if product_size.stock <= 0:
        return redirect("cart_page")

    try:
        quantity = int(
            request.POST.get(
                "quantity",
                1
            )
        )
    except (TypeError, ValueError):
        quantity = 1

    if quantity < 1:
        quantity = 1

    if quantity > product_size.stock:
        quantity = product_size.stock

    new_key = f"{product.id}_{product_size.id}"

    # Same product + same size already exists
    if new_key in guest_cart:

        existing_quantity = int(
            guest_cart[new_key].get(
                "quantity",
                1
            )
        )

        new_quantity = (
            existing_quantity +
            quantity
        )

        if new_quantity > product_size.stock:
            new_quantity = product_size.stock

        guest_cart[new_key]["quantity"] = new_quantity

    else:

        guest_cart[new_key] = {
            "product_id": product.id,
            "size_id": product_size.id,
            "quantity": quantity,
        }

    _save_guest_cart(request, guest_cart)

    return redirect("cart_page")
# =========================================================
# GUEST UPDATE CART SIZE
# =========================================================

def guest_update_cart_size(request, item_key):

    guest_cart = _get_guest_cart(request)


    if item_key not in guest_cart:

        return redirect("cart_page")


    data = guest_cart[item_key]


    product = ProductsModel.objects.filter(
        id=data.get("product_id"),
        is_available=True
    ).first()


    if not product:

        return redirect("cart_page")


    size_id = request.POST.get("size_id")


    if not size_id:

        return redirect("cart_page")


    product_size = ProductSize.objects.filter(
        id=size_id,
        product=product,
        is_available=True
    ).first()


    if not product_size:

        return redirect("cart_page")


    if product_size.stock <= 0:

        return redirect("cart_page")


    quantity = data.get(
        "quantity",
        1
    )


    if quantity > product_size.stock:

        quantity = product_size.stock


    new_key = (
        f"{product.id}_{product_size.id}"
    )


    # Same product + same size already exists
    if (
        new_key != item_key
        and new_key in guest_cart
    ):

        existing_quantity = (
            guest_cart[new_key]["quantity"]
        )


        new_quantity = (
            existing_quantity +
            quantity
        )


        if new_quantity > product_size.stock:

            new_quantity = product_size.stock


        guest_cart[new_key]["quantity"] = (
            new_quantity
        )


        guest_cart.pop(
            item_key,
            None
        )


    else:

        guest_cart[new_key] = {

            "product_id": product.id,

            "size_id": product_size.id,

            "quantity": quantity,

        }


        if new_key != item_key:

            guest_cart.pop(
                item_key,
                None
            )


    _save_guest_cart(
        request,
        guest_cart
    )


    return redirect("cart_page")


# =========================================================
# NAFI CART
# =========================================================
# =========================================================
# ADD TO CART
# =========================================================

def add_to_cart(request, product_id):

    # -----------------------------------------------------
    # GET PRODUCT
    # -----------------------------------------------------

    product = get_object_or_404(
        ProductsModel,
        id=product_id,
        is_available=True
    )


    # -----------------------------------------------------
    # GET SIZE ID
    # -----------------------------------------------------

    size_id = request.POST.get("size_id")

    if not size_id:
        return redirect(
            "product_detail_page",
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
            request.POST.get(
                "quantity",
                1
            )
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
            "product_detail_page",
            slug=product.slug
        )


    if quantity > product_size.stock:

        quantity = product_size.stock


    # =====================================================
    # LOGGED-IN USER
    # =====================================================

    if request.user.is_authenticated:

        cart, created = Cart.objects.get_or_create(
            user=request.user
        )


        cart_item, created = CartItem.objects.get_or_create(

            cart=cart,

            product=product,

            size=product_size.size,

            defaults={
                "quantity": quantity
            }

        )


        if not created:

            new_quantity = (
                cart_item.quantity +
                quantity
            )


            if new_quantity > product_size.stock:

                new_quantity = product_size.stock


            cart_item.quantity = new_quantity

            cart_item.save()


        return redirect("cart_page")


    # =====================================================
    # GUEST USER
    # =====================================================

    guest_cart = _get_guest_cart(request)


    # -----------------------------------------------------
    # UNIQUE CART KEY
    # -----------------------------------------------------

    cart_key = f"{product.id}_{product_size.id}"


    # -----------------------------------------------------
    # EXISTING GUEST ITEM
    # -----------------------------------------------------

    if cart_key in guest_cart:

        new_quantity = (
            guest_cart[cart_key]["quantity"] +
            quantity
        )


        if new_quantity > product_size.stock:

            new_quantity = product_size.stock


        guest_cart[cart_key]["quantity"] = (
            new_quantity
        )


    # -----------------------------------------------------
    # NEW GUEST ITEM
    # -----------------------------------------------------

    else:

        guest_cart[cart_key] = {

            "product_id": product.id,

            "size_id": product_size.id,

            "quantity": quantity,

        }


    # -----------------------------------------------------
    # SAVE SESSION
    # -----------------------------------------------------

    _save_guest_cart(
        request,
        guest_cart
    )


    return redirect("cart_page")
# =========================================================
# CART PAGE
# =========================================================

# =========================================================
# CART PAGE
# =========================================================

def cart_page(request):

    # =====================================================
    # LOGGED-IN USER
    # =====================================================

    if request.user.is_authenticated:

        cart, created = Cart.objects.get_or_create(
            user=request.user
        )


        cart_items = (
            cart.items
            .select_related("product")
            .order_by("-created_at")
        )


        context = {

            "cart": cart,

            "cart_items": cart_items,

            "is_guest_cart": False,

        }


        return render(
            request,
            "customer/cart.html",
            context
        )


    # =====================================================
    # GUEST USER
    # =====================================================

    cart_items = _get_guest_cart_items(
        request
    )


    guest_cart = _get_guest_cart_summary(
        cart_items
    )


    context = {

        "cart": guest_cart,

        "cart_items": cart_items,

        "is_guest_cart": True,

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
        return redirect("customer_login")


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
    # GET CURRENT PRODUCT SIZE
    # -----------------------------------------------------

    product_size = get_object_or_404(
        ProductSize,
        product=cart_item.product,
        size=cart_item.size
    )


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
    # UPDATE QUANTITY
    # -----------------------------------------------------

    cart_item.quantity = quantity

    cart_item.save()


    # -----------------------------------------------------
    # REDIRECT
    # -----------------------------------------------------

    return redirect("cart_page")


# =========================================================
# UPDATE CART SIZE
# =========================================================

def update_cart_size(request, item_id):

    if not request.user.is_authenticated:
        return redirect("customer_login")


    # -----------------------------------------------------
    # GET USER CART
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
    # GET NEW SIZE
    # -----------------------------------------------------

    size_id = request.POST.get("size_id")

    if not size_id:
        return redirect("cart_page")


    # -----------------------------------------------------
    # GET PRODUCT SIZE
    # -----------------------------------------------------

    product_size = get_object_or_404(
        ProductSize,
        id=size_id,
        product=cart_item.product,
        is_available=True
    )


    # -----------------------------------------------------
    # CHECK STOCK
    # -----------------------------------------------------

    if product_size.stock <= 0:
        return redirect("cart_page")


    # -----------------------------------------------------
    # CHECK SAME PRODUCT + SAME SIZE
    # -----------------------------------------------------

    existing_item = CartItem.objects.filter(
        cart=cart,
        product=cart_item.product,
        size=product_size.size
    ).exclude(
        id=cart_item.id
    ).first()


    # -----------------------------------------------------
    # IF SAME SIZE ALREADY EXISTS
    # -----------------------------------------------------

    if existing_item:

        new_quantity = (
            existing_item.quantity +
            cart_item.quantity
        )

        if new_quantity > product_size.stock:
            new_quantity = product_size.stock

        existing_item.quantity = new_quantity
        existing_item.save()

        cart_item.delete()

        return redirect("cart_page")


    # -----------------------------------------------------
    # UPDATE SIZE
    # -----------------------------------------------------

    if cart_item.quantity > product_size.stock:
        cart_item.quantity = product_size.stock


    cart_item.size = product_size.size

    cart_item.save()


    return redirect("cart_page")

# =========================================================
# ADD ANOTHER SIZE FROM CART
# =========================================================

def add_another_size(request, item_id):

    if not request.user.is_authenticated:
        return redirect("customer_login")

    cart = get_object_or_404(
        Cart,
        user=request.user
    )

    cart_item = get_object_or_404(
        CartItem,
        id=item_id,
        cart=cart
    )

    size_id = request.POST.get("size_id")

    if not size_id:
        return redirect("cart_page")

    product_size = get_object_or_404(
        ProductSize,
        id=size_id,
        product=cart_item.product,
        is_available=True
    )

    if product_size.stock <= 0:
        return redirect("cart_page")

    quantity = request.POST.get("quantity", 1)

    try:
        quantity = int(quantity)
    except (TypeError, ValueError):
        quantity = 1

    if quantity < 1:
        quantity = 1

    if quantity > product_size.stock:
        quantity = product_size.stock

    # Check whether this product + size
    # already exists in cart
    existing_item = CartItem.objects.filter(
        cart=cart,
        product=cart_item.product,
        size=product_size.size
    ).first()

    if existing_item:

        new_quantity = (
            existing_item.quantity + quantity
        )

        if new_quantity > product_size.stock:
            new_quantity = product_size.stock

        existing_item.quantity = new_quantity
        existing_item.save()

    else:

        CartItem.objects.create(
            cart=cart,
            product=cart_item.product,
            size=product_size.size,
            quantity=quantity
        )

    return redirect("cart_page")

# =========================================================
# REMOVE CART ITEM
# =========================================================


def remove_from_cart(request, item_id):

    if not request.user.is_authenticated:
        return redirect("customer_login")


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
    # DELETE ITEM
    # -----------------------------------------------------

    cart_item.delete()


    # -----------------------------------------------------
    # REDIRECT
    # -----------------------------------------------------

    return redirect("cart_page")



# =========================================================
# CLEAR CART
# =========================================================


def clear_cart(request):

    if not request.user.is_authenticated:
        return redirect("customer_login")


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


    # -----------------------------------------------------
    # REDIRECT
    # -----------------------------------------------------

    return redirect("cart_page")



# =========================================================
# WISHLIST
# =========================================================

def add_to_wishlist(request, product_id):

    if not request.user.is_authenticated:
        return JsonResponse({
            "success": False,
            "message": "Login required"
        }, status=401)

    product = get_object_or_404(
        ProductsModel,
        id=product_id,
        is_available=True
    )

    wishlist, created = Wishlist.objects.get_or_create(
        user=request.user
    )

    wishlist_item = WishlistItem.objects.filter(
        wishlist=wishlist,
        product=product
    ).first()

    if wishlist_item:
        wishlist_item.delete()
        is_wishlisted = False
    else:
        WishlistItem.objects.create(
            wishlist=wishlist,
            product=product
        )
        is_wishlisted = True

    wishlist_count = wishlist.items.count()

    return JsonResponse({
        "success": True,
        "is_wishlisted": is_wishlisted,
        "wishlist_count": wishlist_count
    })

# =========================================================
# WISHLIST PAGE
# =========================================================


def wishlist_page(request):

    if not request.user.is_authenticated:
        return redirect("customer_login")


    # -----------------------------------------------------
    # GET / CREATE WISHLIST
    # -----------------------------------------------------

    wishlist, created = Wishlist.objects.get_or_create(
        user=request.user
    )


    # -----------------------------------------------------
    # WISHLIST ITEMS
    # -----------------------------------------------------

    wishlist_items = (
        wishlist.items
        .select_related("product")
        .order_by("-created_at")
    )


    # -----------------------------------------------------
    # CONTEXT
    # -----------------------------------------------------

    context = {
        "wishlist": wishlist,
        "wishlist_items": wishlist_items,
    }


    # -----------------------------------------------------
    # RENDER
    # -----------------------------------------------------

    return render(
        request,
        "customer/wishlist.html",
        context
    )

def new_arrivals_page(request):
    new_arrivals = ProductsModel.objects.filter(
        is_available=True
    ).order_by("-created_at")

    for product in new_arrivals:
        product.is_out_of_stock = not product.sizes.filter(
            is_available=True,
            stock__gt=0
        ).exists()

    context = {
        "new_arrivals": new_arrivals,
    }

    return render(request, "customer/new_arrivals_page.html", context)

def all_products_page(request):
    all_products = ProductsModel.objects.filter(
        is_available=True
    ).order_by("-created_at")

    for product in all_products:
        product.is_out_of_stock = not product.sizes.filter(
            is_available=True,
            stock__gt=0
        ).exists()

    context = {
        "all_products": all_products,
    }

    return render(
        request,
        "customer/all_products.html",
        context
    )

# =========================================================
# CHECKOUT PAGE
# =========================================================
def checkout_page(request):

    # =====================================================
    # HANDLE CHECKOUT FORM SUBMISSION
    # =====================================================

    if request.method == "POST":

        from decimal import Decimal
        from django.db import transaction

        # -------------------------------------------------
        # CUSTOMER INFORMATION
        # -------------------------------------------------

        full_name = request.POST.get(
            "full_name",
            ""
        ).strip()

        phone = request.POST.get(
            "phone",
            ""
        ).strip()

        email = request.POST.get(
            "email",
            ""
        ).strip()

        # -------------------------------------------------
        # SHIPPING INFORMATION
        # -------------------------------------------------

        address = request.POST.get(
            "address",
            ""
        ).strip()

        city = request.POST.get(
            "city",
            ""
        ).strip()

        area = request.POST.get(
            "area",
            ""
        ).strip()

        delivery_note = request.POST.get(
            "delivery_note",
            ""
        ).strip()

        # -------------------------------------------------
        # PAYMENT
        # -------------------------------------------------

        payment_method = request.POST.get(
            "payment_method",
            "COD"
        ).strip()

        # =================================================
        # BASIC VALIDATION
        # =================================================

        if not full_name:

            error_message = (
                "Please enter your full name."
            )

        elif not phone:

            error_message = (
                "Please enter your phone number."
            )

        elif not address:

            error_message = (
                "Please enter your full address."
            )

        elif not city:

            error_message = (
                "Please enter your city."
            )

        elif not area:

            error_message = (
                "Please enter your area."
            )

        elif payment_method not in [
            "COD",
            "Online"
        ]:

            error_message = (
                "Invalid payment method."
            )

        else:

            error_message = None

        # =================================================
        # VALIDATION ERROR
        # =================================================

        if error_message:

            # ---------------------------------------------
            # LOGGED-IN USER
            # ---------------------------------------------

            if request.user.is_authenticated:

                cart = Cart.objects.filter(
                    user=request.user
                ).first()

                if not cart:
                    return redirect(
                        "cart_page"
                    )

                cart_items = (
                    cart.items
                    .select_related(
                        "product"
                    )
                    .prefetch_related(
                        "product__sizes"
                    )
                )

                if not cart_items.exists():
                    return redirect(
                        "cart_page"
                    )

                context = {
                    "cart": cart,
                    "cart_items": cart_items,
                    "is_guest_checkout": False,
                    "checkout_error": error_message,
                }

                return render(
                    request,
                    "customer/checkout.html",
                    context
                )

            # ---------------------------------------------
            # GUEST USER
            # ---------------------------------------------

            cart_items = _get_guest_cart_items(
                request
            )

            if not cart_items:
                return redirect(
                    "cart_page"
                )

            cart = _get_guest_cart_summary(
                cart_items
            )

            context = {
                "cart": cart,
                "cart_items": cart_items,
                "is_guest_checkout": True,
                "checkout_error": error_message,
            }

            return render(
                request,
                "customer/checkout.html",
                context
            )

        # =================================================
        # GET CURRENT CART
        # =================================================

        if request.user.is_authenticated:

            cart = Cart.objects.filter(
                user=request.user
            ).first()

            if not cart:
                return redirect(
                    "cart_page"
                )

            cart_items = list(
                cart.items
                .select_related(
                    "product"
                )
                .prefetch_related(
                    "product__sizes"
                )
            )

            if not cart_items:
                return redirect(
                    "cart_page"
                )

            customer = request.user

        else:

            cart_items = _get_guest_cart_items(
                request
            )

            if not cart_items:
                return redirect(
                    "cart_page"
                )

            cart = _get_guest_cart_summary(
                cart_items
            )

            customer = None

        # =================================================
        # CREATE ORDER
        # =================================================

        try:

            with transaction.atomic():

                # -----------------------------------------
                # PREPARE ORDER ITEMS
                # -----------------------------------------

                order_items_data = []

                subtotal = Decimal(
                    "0.00"
                )

                for cart_item in cart_items:

                    product = cart_item.product

                    quantity = int(
                        cart_item.quantity
                    )

                    # -------------------------------------
                    # FIND PRODUCT SIZE
                    # -------------------------------------

                    if request.user.is_authenticated:

                        product_size = (
                            product.sizes
                            .select_for_update()
                            .filter(
                                size=cart_item.size
                            )
                            .first()
                        )

                    else:

                        product_size = (
                            product.sizes
                            .select_for_update()
                            .filter(
                                pk=cart_item.product_size.pk
                            )
                            .first()
                        )

                    # -------------------------------------
                    # CHECK SIZE
                    # -------------------------------------

                    if not product_size:

                        raise ValueError(
                            f"{product.name} - "
                            "selected size is no longer available."
                        )

                    # -------------------------------------
                    # CHECK AVAILABILITY
                    # -------------------------------------

                    if not product_size.is_available:

                        raise ValueError(
                            f"{product.name} - "
                            f"{product_size.size} is currently unavailable."
                        )

                    # -------------------------------------
                    # CHECK STOCK
                    # -------------------------------------

                    if product_size.stock < quantity:

                        raise ValueError(
                            f"{product.name} - "
                            f"only {product_size.stock} piece(s) "
                            f"are available in size "
                            f"{product_size.size}."
                        )

                    # -------------------------------------
                    # PRICE
                    # -------------------------------------

                    unit_price = (
                        product.discount_price
                        if product.discount_price
                        else product.price
                    )

                    unit_price = Decimal(
                        str(unit_price)
                    )

                    item_total = (
                        unit_price * quantity
                    )

                    subtotal += item_total

                    # -------------------------------------
                    # STORE ORDER ITEM DATA
                    # -------------------------------------

                    order_items_data.append({

                        "product": product,

                        "product_name": product.name,

                        "product_code": product.product_code,

                        "size": product_size.size,

                        "quantity": quantity,

                        "unit_price": unit_price,

                        "total_price": item_total,

                        "product_size": product_size,
                    })

                # =================================================
                # DELIVERY + DISCOUNT
                # =================================================

                # Delivery charge will be implemented later.
                delivery_charge = Decimal(
                    "0.00"
                )

                discount = Decimal(
                    "0.00"
                )

                total_amount = (
                    subtotal
                    + delivery_charge
                    - discount
                )

                # =================================================
                # CREATE ORDER
                # =================================================

                order = Order.objects.create(

                    customer=customer,

                    full_name=full_name,

                    phone=phone,

                    email=email,

                    address=address,

                    city=city,

                    area=area,

                    delivery_note=delivery_note,

                    subtotal=subtotal,

                    delivery_charge=delivery_charge,

                    discount=discount,

                    total_amount=total_amount,

                    status="Pending",

                    payment_method=payment_method,

                    payment_status="Pending",
                )

                # =================================================
                # CREATE ORDER ITEMS + REDUCE STOCK
                # =================================================

                for item_data in order_items_data:

                    OrderItem.objects.create(

                        order=order,

                        product=item_data[
                            "product"
                        ],

                        product_name=item_data[
                            "product_name"
                        ],

                        product_code=item_data[
                            "product_code"
                        ],

                        size=item_data[
                            "size"
                        ],

                        quantity=item_data[
                            "quantity"
                        ],

                        unit_price=item_data[
                            "unit_price"
                        ],

                        total_price=item_data[
                            "total_price"
                        ],
                    )

                    # -----------------------------------------
                    # REDUCE SIZE-SPECIFIC STOCK
                    # -----------------------------------------

                    product_size = item_data[
                        "product_size"
                    ]

                    product_size.stock -= (
                        item_data["quantity"]
                    )

                    product_size.save(
                        update_fields=[
                            "stock"
                        ]
                    )

                    # -----------------------------------------
                    # UPDATE PRODUCT TOTAL STOCK
                    # -----------------------------------------

                    total_stock = sum(
                        size.stock
                        for size in product.sizes.all()
                    )

                    product.stock = total_stock

                    product.save(
                        update_fields=[
                            "stock"
                        ]
                    )

                # =================================================
                # CLEAR CART
                # =================================================

                if request.user.is_authenticated:

                    cart.items.all().delete()

                else:

                    _clear_guest_cart(
                        request
                    )

        except ValueError as e:

            # =================================================
            # STOCK / PRODUCT ERROR
            # =================================================

            error_message = str(e)

            # ---------------------------------------------
            # LOGGED-IN USER
            # ---------------------------------------------

            if request.user.is_authenticated:

                cart = Cart.objects.filter(
                    user=request.user
                ).first()

                if not cart:
                    return redirect(
                        "cart_page"
                    )

                cart_items = (
                    cart.items
                    .select_related(
                        "product"
                    )
                    .prefetch_related(
                        "product__sizes"
                    )
                )

                if not cart_items.exists():
                    return redirect(
                        "cart_page"
                    )

                context = {
                    "cart": cart,
                    "cart_items": cart_items,
                    "is_guest_checkout": False,
                    "checkout_error": error_message,
                }

                return render(
                    request,
                    "customer/checkout.html",
                    context
                )

            # ---------------------------------------------
            # GUEST USER
            # ---------------------------------------------

            cart_items = _get_guest_cart_items(
                request
            )

            if not cart_items:
                return redirect(
                    "cart_page"
                )

            cart = _get_guest_cart_summary(
                cart_items
            )

            context = {
                "cart": cart,
                "cart_items": cart_items,
                "is_guest_checkout": True,
                "checkout_error": error_message,
            }

            return render(
                request,
                "customer/checkout.html",
                context
            )

        # =================================================
        # ORDER CREATED SUCCESSFULLY
        # =================================================

        return redirect(
            "order_confirmation",
            order_number=order.order_number
        )

    # =====================================================
    # LOGGED-IN USER
    # =====================================================

    if request.user.is_authenticated:

        cart = Cart.objects.filter(
            user=request.user
        ).first()

        if not cart:
            return redirect(
                "cart_page"
            )

        cart_items = (
            cart.items
            .select_related(
                "product"
            )
            .prefetch_related(
                "product__sizes"
            )
        )

        if not cart_items.exists():
            return redirect(
                "cart_page"
            )

        context = {
            "cart": cart,
            "cart_items": cart_items,
            "is_guest_checkout": False,
        }

        return render(
            request,
            "customer/checkout.html",
            context
        )

    # =====================================================
    # GUEST CHECKOUT
    # =====================================================

    cart_items = _get_guest_cart_items(
        request
    )

    if not cart_items:
        return redirect(
            "cart_page"
        )

    cart = _get_guest_cart_summary(
        cart_items
    )

    context = {
        "cart": cart,
        "cart_items": cart_items,
        "is_guest_checkout": True,
    }

    return render(
        request,
        "customer/checkout.html",
        context
    )

def order_confirmation_page(request, order_number):

    order = get_object_or_404(
        Order,
        order_number=order_number
    )

    context = {
        "order": order,
    }

    return render(
        request,
        "customer/order_confirmation.html",
        context
    )

def my_orders_page(request):
    if not request.user.is_authenticated:
        return redirect("customer_login")

    orders = (
        Order.objects
        .filter(customer=request.user)
        .prefetch_related("items")
        .order_by("-created_at")
    )

    context = {
        "orders": orders,
    }

    return render(
        request,
        "customer/my_orders.html",
        context
    )