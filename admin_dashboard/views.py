from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from .models import *
from django.db.models import Q
from .forms import CategoryForm
from django.db import transaction
from experiment1.models import *



def dashboard_page(request):
    total_products = ProductsModel.objects.count()

    context = {
        'page_title': 'Dashboard',
        'total_products': total_products,

    }


    return render(request, "admin_dashboard/dashboard.html", context)   


def products_page(request):

    # ==========================================
    # GET DATA
    # ==========================================

    search_query = request.GET.get('search', '').strip()
    stock_status = request.GET.get('stock_status', '')

    # ==========================================
    # PRODUCT CARDS
    # ==========================================

    total_products = ProductsModel.objects.count()

    featured_products = ProductsModel.objects.filter(
        is_featured=True
    ).count()

    out_of_stock = ProductsModel.objects.filter(
        stock=0
    ).count()

    available_products = ProductsModel.objects.filter(
        is_available=True
    ).count()


    # ==========================================
    # ALL PRODUCTS
    # ==========================================

    product_data = ProductsModel.objects.all()


    # ==========================================
    # SEARCH
    # Product Name OR Product Code
    # ==========================================

    if search_query:

        product_data = product_data.filter(
            Q(name__icontains=search_query) |
            Q(product_code__icontains=search_query)
        )


    # ==========================================
    # STOCK FILTER
    # ==========================================

    if stock_status == 'in_stock':

        product_data = product_data.filter(
            stock__gt=0
        )

    elif stock_status == 'out_of_stock':

        product_data = product_data.filter(
            stock=0
        )


    # ==========================================
    # CONTEXT
    # ==========================================

    context = {
        'product_data': product_data,
        'page_title': 'Products',

        'search_query': search_query,
        'stock_status': stock_status,


        # Cards
        'total_products': total_products,
        'featured_products': featured_products,
        'out_of_stock': out_of_stock,
        'available_products': available_products,
    }


    # ==========================================
    # RENDER
    # ==========================================

    return render(
        request,
        'admin_dashboard/products.html',
        context
    )


def add_product_page(request):

    categories = Category.objects.filter(
        is_active=True
    ).order_by("name")

    product = None

    if request.method == "POST":

        # ==========================================
        # BASIC PRODUCT DATA
        # ==========================================

        product_name = request.POST.get(
            "product_name",
            ""
        ).strip()

        description = request.POST.get(
            "description",
            ""
        ).strip()

        price = request.POST.get(
            "price"
        )

        discount_price = (
            request.POST.get("discount_price")
            or None
        )

        category_id = request.POST.get(
            "category"
        )

        is_available = (
            "is_available" in request.POST
        )

        is_featured = (
            "is_featured" in request.POST
        )


        # ==========================================
        # PRODUCT IMAGES
        # ==========================================

        # Main Image
        main_image = request.FILES.get(
            "main_image"
        )

        # Secondary Image
        secondary_image = request.FILES.get(
            "secondary_image"
        )

        # Gallery Images - Optional
        gallery_images = request.FILES.getlist(
            "gallery_images"
        )


        # ==========================================
        # IMAGE VALIDATION
        # ==========================================

        # Main image is required
        if main_image is None:

            messages.error(
                request,
                "Please upload a main image."
            )

            return redirect(
                "add_product_page"
            )


        # Secondary image is required
        if secondary_image is None:

            messages.error(
                request,
                "Please upload a secondary image."
            )

            return redirect(
                "add_product_page"
            )


        # ==========================================
        # SIZE-WISE STOCK
        # ==========================================

        size_stock = {}

        for size in ["M", "L", "XL", "XXL"]:

            # Check whether this size was selected
            size_selected = (
                f"size_{size}" in request.POST
            )

            # If size is not selected,
            # skip it completely
            if not size_selected:
                continue


            # Get stock for selected size
            stock_value = request.POST.get(
                f"stock_{size}",
                "0"
            )


            # Convert stock to integer
            try:

                stock_value = int(
                    stock_value or 0
                )

            except (ValueError, TypeError):

                stock_value = 0


            # Selected size must have stock
            if stock_value <= 0:

                messages.error(
                    request,
                    f"Please enter valid stock for size {size}."
                )

                return redirect(
                    "add_product_page"
                )


            # Store size and stock
            size_stock[size] = stock_value


        # ==========================================
        # SIZE VALIDATION
        # ==========================================

        if not size_stock:

            messages.error(
                request,
                "Please select at least one size and enter its stock."
            )

            return redirect(
                "add_product_page"
            )


        # ==========================================
        # TOTAL STOCK
        # ==========================================

        total_stock = sum(
            size_stock.values()
        )


        # ==========================================
        # CREATE PRODUCT + IMAGES + SIZES
        # ==========================================

        with transaction.atomic():

            # ======================================
            # CREATE MAIN PRODUCT
            # ======================================

            product = ProductsModel.objects.create(

                name=product_name,

                description=description,

                price=price,

                discount_price=discount_price,

                stock=total_stock,

                # MAIN IMAGE
                image=main_image,

                is_available=is_available,

                is_featured=is_featured,

                category_id=category_id,
            )


            # ======================================
            # CREATE SECONDARY IMAGE
            # ======================================

            ProductImage.objects.create(

                product=product,

                image=secondary_image,

                image_type="secondary",

                sort_order=0,
            )


            # ======================================
            # CREATE GALLERY IMAGES
            # ======================================

            for index, gallery_image in enumerate(
                gallery_images,
                start=1
            ):

                ProductImage.objects.create(

                    product=product,

                    image=gallery_image,

                    image_type="gallery",

                    sort_order=index,
                )


            # ======================================
            # CREATE PRODUCT SIZE RECORDS
            # ======================================

            for size, stock in size_stock.items():

                ProductSize.objects.create(

                    product=product,

                    size=size,

                    stock=stock,

                    is_available=True,
                )


        # ==========================================
        # SAVE ACTION
        # ==========================================

        action = request.POST.get(
            "save_action"
        )


        # ==========================================
        # SAVE
        # ==========================================

        if action == "save":

            messages.success(
                request,
                "Product added successfully."
            )

            return redirect(
                "products_page"
            )


        # ==========================================
        # SAVE & ADD ANOTHER
        # ==========================================

        elif action == "save_add":

            messages.success(
                request,
                "Product added successfully."
            )

            return redirect(
                "add_product_page"
            )


        # ==========================================
        # SAVE & CONTINUE EDITING
        # ==========================================

        elif action == "save_edit":

            messages.success(
                request,
                "Product added successfully."
            )

            return redirect(
                "edit_product_page",
                product.id
            )


    # ==========================================
    # CONTEXT
    # ==========================================

    context = {

        "product": product,

        "page_title": "Products",

        "categories": categories,
    }


    # ==========================================
    # RENDER
    # ==========================================

    return render(
        request,
        "admin_dashboard/add_product.html",
        context
    )



def edit_product_page(request, id):

    # ==========================================================
    # GET PRODUCT
    # ==========================================================

    product = get_object_or_404(
        ProductsModel,
        id=id
    )


    # ==========================================================
    # GET CATEGORIES
    # ==========================================================

    categories = Category.objects.filter(
        Q(is_active=True) |
        Q(id=product.category_id)
    ).order_by("name")


    # ==========================================================
    # GET EXISTING SIZES
    # ==========================================================

    existing_sizes = {
        item.size: item
        for item in product.sizes.all()
    }


    # ==========================================================
    # GET SECONDARY IMAGE
    # ==========================================================

    secondary_image = (
        product.images
        .filter(
            image_type="secondary"
        )
        .first()
    )


    # ==========================================================
    # GET GALLERY IMAGES
    # ==========================================================

    gallery_images = (
        product.images
        .filter(
            image_type="gallery"
        )
        .order_by(
            "sort_order",
            "id"
        )
    )


    # ==========================================================
    # POST
    # ==========================================================

    if request.method == "POST":

        # ======================================================
        # BASIC PRODUCT DATA
        # ======================================================

        product_name = request.POST.get(
            "product_name",
            ""
        ).strip()

        description = request.POST.get(
            "description",
            ""
        ).strip()

        price = request.POST.get(
            "price"
        )

        discount_price = (
            request.POST.get(
                "discount_price"
            )
            or None
        )

        category_id = request.POST.get(
            "category"
        )

        is_available = (
            "is_available" in request.POST
        )

        is_featured = (
            "is_featured" in request.POST
        )


        # ======================================================
        # IMAGE FILES
        # ======================================================

        # Main image
        main_image = request.FILES.get(
            "main_image"
        )


        # Secondary image
        secondary_image_upload = (
            request.FILES.get(
                "secondary_image"
            )
        )


        # New gallery images
        gallery_images_upload = (
            request.FILES.getlist(
                "gallery_images"
            )
        )


        # ======================================================
        # GALLERY IMAGE REPLACE
        # ======================================================

        # Existing gallery image IDs
        gallery_replace_ids = request.POST.getlist(
            "gallery_replace_ids[]"
        )

        # New files corresponding to those IDs
        gallery_replace_files = request.FILES.getlist(
            "gallery_replace_files[]"
        )


        # ------------------------------------------------------
        # Fallback
        # ------------------------------------------------------
        # If JS sends without [] Django will still support it.

        if not gallery_replace_ids:
            gallery_replace_ids = request.POST.getlist(
                "gallery_replace_ids"
            )

        if not gallery_replace_files:
            gallery_replace_files = request.FILES.getlist(
                "gallery_replace_files"
            )


        # ======================================================
        # GALLERY REORDER
        # ======================================================

        gallery_order = request.POST.getlist(
            "gallery_order[]"
        )


        # ------------------------------------------------------
        # Fallback for comma-separated order
        # ------------------------------------------------------

        if not gallery_order:

            gallery_order_string = request.POST.get(
                "gallery_order",
                ""
            ).strip()

            if gallery_order_string:

                gallery_order = [
                    item.strip()
                    for item in gallery_order_string.split(",")
                    if item.strip()
                ]


        # ======================================================
        # EXISTING IMAGE DELETE REQUESTS
        # ======================================================

        delete_image_ids = request.POST.getlist(
            "delete_image_ids"
        )


        # ======================================================
        # SIZE-WISE STOCK
        # ======================================================

        size_stock = {}


        for size in [
            "M",
            "L",
            "XL",
            "XXL"
        ]:

            # --------------------------------------------------
            # Check selected size
            # --------------------------------------------------

            size_selected = (
                f"size_{size}" in request.POST
            )


            if not size_selected:
                continue


            # --------------------------------------------------
            # Get stock
            # --------------------------------------------------

            stock_value = request.POST.get(
                f"stock_{size}",
                "0"
            )


            try:

                stock_value = int(
                    stock_value or 0
                )

            except (
                ValueError,
                TypeError
            ):

                stock_value = 0


            # --------------------------------------------------
            # Validate stock
            # --------------------------------------------------

            if stock_value <= 0:

                messages.error(
                    request,
                    f"Please enter valid stock for size {size}."
                )

                return redirect(
                    "edit_product_page",
                    id=product.id
                )


            size_stock[size] = stock_value


        # ======================================================
        # SIZE VALIDATION
        # ======================================================

        if not size_stock:

            messages.error(
                request,
                "Please select at least one size and enter its stock."
            )

            return redirect(
                "edit_product_page",
                id=product.id
            )


        # ======================================================
        # TOTAL STOCK
        # ======================================================

        total_stock = sum(
            size_stock.values()
        )


        # ======================================================
        # UPDATE BASIC PRODUCT DATA
        # ======================================================

        product.name = product_name

        product.description = description

        product.price = price

        product.discount_price = discount_price

        product.stock = total_stock

        product.category_id = category_id

        product.is_available = is_available

        product.is_featured = is_featured


        # ======================================================
        # UPDATE MAIN IMAGE
        # ======================================================

        if main_image:

            old_main_image = product.image

            product.image = main_image

            # Save first so new Cloudinary image
            # is uploaded successfully.
            product.save()


            # --------------------------------------------------
            # Delete old main image
            # --------------------------------------------------

            if (
                old_main_image
                and old_main_image.name
            ):

                try:

                    old_main_image.storage.delete(
                        old_main_image.name
                    )

                except Exception:

                    pass

        else:

            product.save()


        # ======================================================
        # DELETE SELECTED EXISTING IMAGES
        # ======================================================

        if delete_image_ids:

            images_to_delete = (
                ProductImage.objects.filter(
                    product=product,
                    id__in=delete_image_ids,
                    image_type__in=[
                        "secondary",
                        "gallery"
                    ]
                )
            )


            for image_obj in images_to_delete:

                # --------------------------------------------------
                # Delete Cloudinary file
                # --------------------------------------------------

                if image_obj.image:

                    try:

                        image_obj.image.storage.delete(
                            image_obj.image.name
                        )

                    except Exception:

                        pass


                # --------------------------------------------------
                # Delete database record
                # --------------------------------------------------

                image_obj.delete()


        # ======================================================
        # UPDATE / REPLACE SECONDARY IMAGE
        # ======================================================

        if secondary_image_upload:

            # --------------------------------------------------
            # Get current secondary image
            # --------------------------------------------------

            current_secondary = (
                ProductImage.objects.filter(
                    product=product,
                    image_type="secondary"
                )
                .first()
            )


            # --------------------------------------------------
            # Existing secondary
            # --------------------------------------------------

            if current_secondary:

                old_secondary_image = (
                    current_secondary.image
                )


                current_secondary.image = (
                    secondary_image_upload
                )

                current_secondary.sort_order = 0

                current_secondary.save()


                # --------------------------------------------------
                # Delete old Cloudinary image
                # --------------------------------------------------

                if (
                    old_secondary_image
                    and old_secondary_image.name
                ):

                    try:

                        old_secondary_image.storage.delete(
                            old_secondary_image.name
                        )

                    except Exception:

                        pass


            # --------------------------------------------------
            # No secondary image yet
            # --------------------------------------------------

            else:

                ProductImage.objects.create(
                    product=product,
                    image=secondary_image_upload,
                    image_type="secondary",
                    sort_order=0
                )


        # ======================================================
        # REPLACE INDIVIDUAL GALLERY IMAGES
        # ======================================================

        if (
            gallery_replace_ids
            and gallery_replace_files
        ):

            # --------------------------------------------------
            # Pair image ID + uploaded file
            # --------------------------------------------------

            for image_id, new_image_file in zip(
                gallery_replace_ids,
                gallery_replace_files
            ):

                # ----------------------------------------------
                # Validate ID
                # ----------------------------------------------

                try:

                    image_id = int(
                        image_id
                    )

                except (
                    ValueError,
                    TypeError
                ):

                    continue


                # ----------------------------------------------
                # Never allow deleted image to be replaced
                # ----------------------------------------------

                if str(image_id) in delete_image_ids:

                    continue


                # ----------------------------------------------
                # Get only this product's gallery image
                # ----------------------------------------------

                gallery_image = (
                    ProductImage.objects.filter(
                        id=image_id,
                        product=product,
                        image_type="gallery"
                    )
                    .first()
                )


                if not gallery_image:
                    continue


                # ----------------------------------------------
                # Keep old image reference
                # ----------------------------------------------

                old_gallery_image = (
                    gallery_image.image
                )


                # ----------------------------------------------
                # Replace image
                # ----------------------------------------------

                gallery_image.image = (
                    new_image_file
                )

                gallery_image.save()


                # ----------------------------------------------
                # Delete old Cloudinary image
                # ----------------------------------------------

                if (
                    old_gallery_image
                    and old_gallery_image.name
                ):

                    try:

                        old_gallery_image.storage.delete(
                            old_gallery_image.name
                        )

                    except Exception:

                        pass


        # ======================================================
        # NORMALIZE EXISTING GALLERY ORDER
        # ======================================================

        gallery_queryset = (
            ProductImage.objects.filter(
                product=product,
                image_type="gallery"
            )
            .order_by(
                "sort_order",
                "id"
            )
        )


        # ======================================================
        # REORDER GALLERY IMAGES
        # ======================================================

        if gallery_order:

            # ----------------------------------------------
            # Convert submitted IDs to integers
            # ----------------------------------------------

            submitted_ids = []

            for image_id in gallery_order:

                try:

                    submitted_ids.append(
                        int(image_id)
                    )

                except (
                    ValueError,
                    TypeError
                ):

                    continue


            # ----------------------------------------------
            # Get current gallery IDs
            # ----------------------------------------------

            current_ids = list(
                gallery_queryset.values_list(
                    "id",
                    flat=True
                )
            )


            # ----------------------------------------------
            # Validate submitted order
            #
            # The IDs must represent the existing
            # gallery images after deletion.
            # ----------------------------------------------

            if (
                set(submitted_ids)
                == set(current_ids)
                and len(submitted_ids)
                == len(current_ids)
            ):

                # ------------------------------------------
                # Temporarily move all sort orders
                #
                # This avoids possible uniqueness issues
                # if a future constraint is added.
                # ------------------------------------------

                for image_obj in gallery_queryset:

                    image_obj.sort_order = (
                        image_obj.sort_order + 100000
                    )

                    image_obj.save(
                        update_fields=[
                            "sort_order"
                        ]
                    )


                # ------------------------------------------
                # Save new order
                # ------------------------------------------

                for sort_order, image_id in enumerate(
                    submitted_ids
                ):

                    ProductImage.objects.filter(
                        id=image_id,
                        product=product,
                        image_type="gallery"
                    ).update(
                        sort_order=sort_order
                    )


        # ======================================================
        # NORMALIZE GALLERY ORDER
        #
        # This keeps sort_order clean:
        #
        # 0, 1, 2, 3...
        #
        # instead of:
        #
        # 0, 4, 7, 9...
        # ======================================================

        gallery_queryset = (
            ProductImage.objects.filter(
                product=product,
                image_type="gallery"
            )
            .order_by(
                "sort_order",
                "id"
            )
        )


        for sort_order, image_obj in enumerate(
            gallery_queryset
        ):

            if image_obj.sort_order != sort_order:

                ProductImage.objects.filter(
                    id=image_obj.id
                ).update(
                    sort_order=sort_order
                )


        # ======================================================
        # ADD NEW GALLERY IMAGES
        # ======================================================

        if gallery_images_upload:

            # --------------------------------------------------
            # Find current highest sort order
            # --------------------------------------------------

            last_gallery = (
                ProductImage.objects.filter(
                    product=product,
                    image_type="gallery"
                )
                .order_by(
                    "-sort_order"
                )
                .first()
            )


            if last_gallery:

                next_sort_order = (
                    last_gallery.sort_order + 1
                )

            else:

                next_sort_order = 0


            # --------------------------------------------------
            # Save new gallery images
            # --------------------------------------------------

            for index, image_file in enumerate(
                gallery_images_upload
            ):

                ProductImage.objects.create(
                    product=product,
                    image=image_file,
                    image_type="gallery",
                    sort_order=(
                        next_sort_order + index
                    )
                )


        # ======================================================
        # UPDATE PRODUCT SIZES
        # ======================================================

        for size in [
            "M",
            "L",
            "XL",
            "XXL"
        ]:

            # --------------------------------------------------
            # Selected size
            # --------------------------------------------------

            if size in size_stock:

                ProductSize.objects.update_or_create(
                    product=product,
                    size=size,
                    defaults={
                        "stock": size_stock[size],
                        "is_available": True,
                    }
                )


            # --------------------------------------------------
            # Unselected size
            # --------------------------------------------------

            else:

                ProductSize.objects.filter(
                    product=product,
                    size=size
                ).delete()


        # ======================================================
        # SAVE ACTION
        # ======================================================

        action = request.POST.get(
            "save_action"
        )


        # ======================================================
        # SAVE
        # ======================================================

        if action == "save":

            messages.success(
                request,
                "Product updated successfully."
            )

            return redirect(
                "products_page"
            )


        # ======================================================
        # SAVE & ADD ANOTHER
        # ======================================================

        elif action == "save_add":

            messages.success(
                request,
                "Product updated successfully."
            )

            return redirect(
                "add_product_page"
            )


        # ======================================================
        # SAVE & CONTINUE EDITING
        # ======================================================

        elif action == "save_edit":

            messages.success(
                request,
                "Product updated successfully."
            )

            return redirect(
                "edit_product_page",
                id=product.id
            )


        # ======================================================
        # DEFAULT
        # ======================================================

        else:

            messages.success(
                request,
                "Product updated successfully."
            )

            return redirect(
                "products_page"
            )


    # ==========================================================
    # REFRESH IMAGE DATA
    # ==========================================================

    secondary_image = (
        product.images
        .filter(
            image_type="secondary"
        )
        .first()
    )


    gallery_images = (
        product.images
        .filter(
            image_type="gallery"
        )
        .order_by(
            "sort_order",
            "id"
        )
    )


    # ==========================================================
    # REFRESH EXISTING SIZES
    # ==========================================================

    existing_sizes = {
        item.size: item
        for item in product.sizes.all()
    }


    # ==========================================================
    # CONTEXT
    # ==========================================================

    context = {

        "product": product,

        "page_title": "Products",

        "categories": categories,

        "existing_sizes": existing_sizes,

        "secondary_image": secondary_image,

        "gallery_images": gallery_images,

    }


    # ==========================================================
    # RENDER
    # ==========================================================

    return render(
        request,
        "admin_dashboard/edit_product.html",
        context
    )


def delete_product_page(request, id):


    product = get_object_or_404(ProductsModel, id=id)



    if product is None:
        messages.warning(
            request, "It may have already been deleted." )
        return redirect("products_page")

    product.delete()

    messages.success(request, "Product deleted successfully.")

    return redirect("products_page")


def categories_page(request):

    search_query = request.GET.get('search', '').strip()

    # Status Filter
    status_filter = request.GET.get('status', '')

    # Base Query
    category_data = Category.objects.all()

    # Search
    if search_query:
        category_data = category_data.filter(
            Q(name__icontains=search_query) 
        )

    # Status Filter
    if status_filter == 'active':
        category_data = category_data.filter(
            is_active=True
        )

    elif status_filter == 'inactive':
        category_data = category_data.filter(
            is_active=False
        )

    # Order
    category_data = category_data.order_by('-created_at')

    # Summary Cards
    total_categories = Category.objects.count()

    active_categories = Category.objects.filter(
        is_active=True
    ).count()

    inactive_categories = Category.objects.filter(
        is_active=False
    ).count()

    total_products = ProductsModel.objects.count()

    context = {
        'category_data': category_data,
        'page_title': 'Categories',

        'total_categories': total_categories,
        'active_categories': active_categories,
        'inactive_categories': inactive_categories,
        'total_products': total_products,

        'search_query': search_query,
        'status_filter': status_filter,
    }

    return render(
        request,
        'admin_dashboard/categories.html',
        context
    )



def add_category(request):

    if request.method == 'POST':

        form = CategoryForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()

            return redirect('categories_page')

    else:
        form = CategoryForm()


    context = {
        'form': form,
        'page_title' : "Categories"
    }

    return render(
        request,
        'admin_dashboard/add_categories.html',
        context
    )

def edit_category(request, id):

    category = get_object_or_404(Category, id=id)

    if request.method == "POST":

        form = CategoryForm(
            request.POST,
            request.FILES,
            instance=category
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Category updated successfully."
            )

            return redirect("categories_page")

    else:
        form = CategoryForm(instance=category)

    context = {
        "form": form,
        "category": category,
        "page_title": "Categories",
    }

    return render(
        request,
        "admin_dashboard/edit_categories.html",
        context
    )


def delete_category(request, id):


    category = get_object_or_404(Category, id=id)

    if category is None:
        messages.warning(
            request, "It may have already been deleted." )
        return redirect("products_page")

    category.delete()

    messages.success(request, "Category deleted successfully.")

    return redirect("categories_page")



def orders_page(request):

    return render(request, 'admin_dashboard/orders.html', { "page_title": "Orders" })   




def customers_page(request):

    return render(request, 'admin_dashboard/customers.html', { "page_title": "Customers" })



def inventory_page(request):

    return render(request, 'admin_dashboard/inventory.html', { "page_title": "Inventory" })  




def coupons_page(request):

    return render(request, 'admin_dashboard/coupons.html', { "page_title": "Coupons" })   



def reviews_page(request):

    return render(request, 'admin_dashboard/reviews.html', { "page_title": "Reviews" })    




def reports_page(request):

    return render(request, 'admin_dashboard/reports.html', { "page_title": "Reports" })




def settings_page(request):

    return render(request, 'admin_dashboard/settings.html', { "page_title": "Settings" })

def admin_users_page(request):

    return render(request, 'admin_dashboard/admin_users.html', { "page_title": "Admin Users" })



def hidden_sidebar_page(request):
    return render(request, 'admin_dashboard/master/hidden_sidebar.html')

def logout_page(request):
    logout(request)
    return redirect("home_page")


# =========================================================
# ABOUT PAGE MANAGEMENT
# =========================================================

def about_management(request):
    """
    Main About Page management screen.
    Content is managed from the custom admin dashboard.
    """

    about = AboutPage.objects.first()

    if not about:
        about = AboutPage.objects.create(
            is_published=True
        )

    values = about.values.all()
    quality_items = about.quality_items.all()
    journey_items = about.journey_items.all()

    context = {
        "about": about,
        'page_title': 'About',
        "values": values,
        "quality_items": quality_items,
        "journey_items": journey_items,
    }

    return render(
        request,
        "admin_dashboard/about_management.html",
        context,
    )


# =========================================================
# UPDATE MAIN ABOUT PAGE
# =========================================================

def update_about_page(request):

    if request.method != "POST":
        return redirect("about_management")

    about = get_object_or_404(
        AboutPage,
        id=request.POST.get("about_id")
    )

    # -----------------------------------------------------
    # HERO
    # -----------------------------------------------------

    about.hero_eyebrow = request.POST.get(
        "hero_eyebrow", ""
    )

    about.hero_title = request.POST.get(
        "hero_title", ""
    )

    about.hero_description = request.POST.get(
        "hero_description", ""
    )

    if request.FILES.get("hero_image"):
        about.hero_image = request.FILES["hero_image"]


    # -----------------------------------------------------
    # WHO WE ARE
    # -----------------------------------------------------

    about.who_title = request.POST.get(
        "who_title", ""
    )

    about.who_content = request.POST.get(
        "who_content", ""
    )

    if request.FILES.get("who_image"):
        about.who_image = request.FILES["who_image"]


    # -----------------------------------------------------
    # BRAND ORIGIN
    # -----------------------------------------------------

    about.origin_title = request.POST.get(
        "origin_title", ""
    )

    about.origin_content = request.POST.get(
        "origin_content", ""
    )


    # -----------------------------------------------------
    # VISION
    # -----------------------------------------------------

    about.vision_title = request.POST.get(
        "vision_title", ""
    )

    about.vision_statement = request.POST.get(
        "vision_statement", ""
    )

    about.vision_content = request.POST.get(
        "vision_content", ""
    )


    # -----------------------------------------------------
    # MODERN MAN
    # -----------------------------------------------------

    about.modern_title = request.POST.get(
        "modern_title", ""
    )

    about.modern_content = request.POST.get(
        "modern_content", ""
    )


    # -----------------------------------------------------
    # NAFI AESTHETIC
    # -----------------------------------------------------

    about.aesthetic_title = request.POST.get(
        "aesthetic_title", ""
    )

    about.aesthetic_content = request.POST.get(
        "aesthetic_content", ""
    )

    if request.FILES.get("aesthetic_image"):
        about.aesthetic_image = request.FILES[
            "aesthetic_image"
        ]


    # -----------------------------------------------------
    # QUALITY
    # -----------------------------------------------------

    about.quality_title = request.POST.get(
        "quality_title", ""
    )

    about.quality_intro = request.POST.get(
        "quality_intro", ""
    )


    # -----------------------------------------------------
    # TRANSPARENCY
    # -----------------------------------------------------

    about.transparency_title = request.POST.get(
        "transparency_title", ""
    )

    about.transparency_content = request.POST.get(
        "transparency_content", ""
    )


    # -----------------------------------------------------
    # WHY NAFI
    # -----------------------------------------------------

    about.why_title = request.POST.get(
        "why_title", ""
    )

    about.why_content = request.POST.get(
        "why_content", ""
    )


    # -----------------------------------------------------
    # NAFI AT A GLANCE
    # -----------------------------------------------------

    about.profile_title = request.POST.get(
        "profile_title", ""
    )

    about.profile_category = request.POST.get(
        "profile_category", ""
    )

    about.profile_focus = request.POST.get(
        "profile_focus", ""
    )

    about.profile_style = request.POST.get(
        "profile_style", ""
    )

    about.profile_values = request.POST.get(
        "profile_values", ""
    )

    about.profile_products = request.POST.get(
        "profile_products", ""
    )


    # -----------------------------------------------------
    # FINAL BRAND STATEMENT
    # -----------------------------------------------------

    about.final_title = request.POST.get(
        "final_title", ""
    )

    about.final_content = request.POST.get(
        "final_content", ""
    )

    about.final_statement = request.POST.get(
        "final_statement", ""
    )

    about.cta_text = request.POST.get(
        "cta_text", ""
    )

    if request.FILES.get("final_image"):
        about.final_image = request.FILES[
            "final_image"
        ]


    # -----------------------------------------------------
    # PUBLISH STATUS
    # -----------------------------------------------------

    about.is_published = (
        request.POST.get("is_published") == "on"
    )


    about.save()

    messages.success(
        request,
        "About page updated successfully."
    )

    return redirect("about_management")


# =========================================================
# ADD BRAND VALUE
# =========================================================

def add_about_value(request):

    if request.method == "POST":

        about = get_object_or_404(
            AboutPage,
            id=request.POST.get("about_id")
        )

        AboutValue.objects.create(
            about_page=about,
            title=request.POST.get("title", ""),
            description=request.POST.get(
                "description", ""
            ),
            icon=request.POST.get("icon", ""),
            display_order=request.POST.get(
                "display_order", 0
            ) or 0,
            is_active=True,
        )

        messages.success(
            request,
            "Brand value added successfully."
        )

    return redirect("about_management")


# =========================================================
# DELETE BRAND VALUE
# =========================================================

def delete_about_value(request, value_id):

    if request.method == "POST":

        value = get_object_or_404(
            AboutValue,
            id=value_id
        )

        value.delete()

        messages.success(
            request,
            "Brand value deleted successfully."
        )

    return redirect("about_management")

# =========================================================
# UPDATE BRAND VALUE
# =========================================================

def update_about_value(request, value_id):

    if request.method == "POST":

        value = get_object_or_404(
            AboutValue,
            id=value_id
        )

        value.title = request.POST.get(
            "title",
            ""
        )

        value.description = request.POST.get(
            "description",
            ""
        )

        value.icon = request.POST.get(
            "icon",
            ""
        )

        value.display_order = request.POST.get(
            "display_order",
            0
        ) or 0

        value.is_active = (
            request.POST.get("is_active") == "on"
        )

        value.save()

        messages.success(
            request,
            "Brand value updated successfully."
        )

    return redirect("about_management")

# =========================================================
# ADD QUALITY COMMITMENT
# =========================================================

def add_about_quality(request):

    if request.method == "POST":

        about = get_object_or_404(
            AboutPage,
            id=request.POST.get("about_id")
        )

        AboutQuality.objects.create(
            about_page=about,
            title=request.POST.get("title", ""),
            description=request.POST.get(
                "description", ""
            ),
            icon=request.POST.get("icon", ""),
            display_order=request.POST.get(
                "display_order", 0
            ) or 0,
            is_active=True,
        )

        messages.success(
            request,
            "Quality commitment added successfully."
        )

    return redirect("about_management")


# =========================================================
# DELETE QUALITY COMMITMENT
# =========================================================

def delete_about_quality(request, quality_id):

    if request.method == "POST":

        quality = get_object_or_404(
            AboutQuality,
            id=quality_id
        )

        quality.delete()

        messages.success(
            request,
            "Quality commitment deleted successfully."
        )

    return redirect("about_management")

# =========================================================
# UPDATE QUALITY COMMITMENT
# =========================================================

def update_about_quality(request, quality_id):

    if request.method == "POST":

        quality = get_object_or_404(
            AboutQuality,
            id=quality_id
        )

        quality.title = request.POST.get(
            "title",
            ""
        )

        quality.description = request.POST.get(
            "description",
            ""
        )

        quality.icon = request.POST.get(
            "icon",
            ""
        )

        quality.display_order = request.POST.get(
            "display_order",
            0
        ) or 0

        quality.is_active = (
            request.POST.get("is_active") == "on"
        )

        quality.save()

        messages.success(
            request,
            "Quality commitment updated successfully."
        )

    return redirect("about_management")
# =========================================================
# ADD JOURNEY ITEM
# =========================================================

def add_about_journey(request):

    if request.method == "POST":

        about = get_object_or_404(
            AboutPage,
            id=request.POST.get("about_id")
        )

        journey = AboutJourney.objects.create(
            about_page=about,
            year=request.POST.get("year", ""),
            title=request.POST.get("title", ""),
            description=request.POST.get(
                "description", ""
            ),
            display_order=request.POST.get(
                "display_order", 0
            ) or 0,
            is_active=True,
        )

        if request.FILES.get("image"):
            journey.image = request.FILES["image"]
            journey.save()

        messages.success(
            request,
            "Journey item added successfully."
        )

    return redirect("about_management")


# =========================================================
# DELETE JOURNEY ITEM
# =========================================================

def delete_about_journey(request, journey_id):

    if request.method == "POST":

        journey = get_object_or_404(
            AboutJourney,
            id=journey_id
        )

        journey.delete()

        messages.success(
            request,
            "Journey item deleted successfully."
        )

    return redirect("about_management")

# =========================================================
# UPDATE JOURNEY ITEM
# =========================================================

def update_about_journey(request, journey_id):

    if request.method == "POST":

        journey = get_object_or_404(
            AboutJourney,
            id=journey_id
        )

        # -------------------------------------------------
        # BASIC INFORMATION
        # -------------------------------------------------

        journey.year = request.POST.get(
            "year",
            ""
        )

        journey.title = request.POST.get(
            "title",
            ""
        )

        journey.description = request.POST.get(
            "description",
            ""
        )

        # -------------------------------------------------
        # DISPLAY ORDER
        # -------------------------------------------------

        journey.display_order = request.POST.get(
            "display_order",
            0
        ) or 0

        # -------------------------------------------------
        # ACTIVE / INACTIVE
        # -------------------------------------------------

        journey.is_active = (
            request.POST.get("is_active") == "on"
        )

        # -------------------------------------------------
        # IMAGE
        # -------------------------------------------------

        if request.FILES.get("image"):

            journey.image = request.FILES["image"]

        # -------------------------------------------------
        # SAVE
        # -------------------------------------------------

        journey.save()

        messages.success(
            request,
            "Journey item updated successfully."
        )

    return redirect("about_management")



# --------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------
# Setting section
# --------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------
def home_management(request):
    """
    Home Page management screen.
    """

    home_page = HomePage.objects.first()

    if not home_page:
        home_page = HomePage.objects.create()

    hero_slides = home_page.hero_slides.all().order_by(
        "display_order",
        "-created_at"
    )

    context = {
        "page_title": "Home Page",
        "home_page": home_page,
        "hero_slides": hero_slides,
    }

    return render(
        request,
        "admin_dashboard/home_management.html",
        context
    )

def update_home_page(request):
    """
    Update homepage text, section visibility,
    and second hero image settings.
    """

    home_page = HomePage.objects.first()

    if not home_page:
        home_page = HomePage.objects.create()

    if request.method == "POST":

        # ==========================================
        # HERO CONTENT
        # ==========================================

        home_page.hero_subtitle = request.POST.get(
            "hero_subtitle",
            ""
        ).strip()

        home_page.hero_title = request.POST.get(
            "hero_title",
            ""
        ).strip()

        home_page.hero_button_text = request.POST.get(
            "hero_button_text",
            ""
        ).strip()

        home_page.hero_button_link = request.POST.get(
            "hero_button_link",
            ""
        ).strip()

        # ==========================================
        # SECTION VISIBILITY
        # ==========================================

        home_page.hero_is_active = (
            request.POST.get("hero_is_active") == "on"
        )

        home_page.categories_is_active = (
            request.POST.get("categories_is_active") == "on"
        )

        home_page.featured_is_active = (
            request.POST.get("featured_is_active") == "on"
        )

        home_page.new_arrivals_is_active = (
            request.POST.get("new_arrivals_is_active") == "on"
        )

        # ==========================================
        # SECOND HERO VISIBILITY
        # ==========================================

        home_page.second_hero_is_active = (
            request.POST.get("second_hero_is_active") == "on"
        )

        # ==========================================
        # SECOND HERO IMAGE
        # ==========================================

        second_hero_image = request.FILES.get(
            "second_hero_image"
        )

        if second_hero_image:
            home_page.second_hero_image = second_hero_image

        # ==========================================
        # SAVE
        # ==========================================
        home_page.full_clean()
        home_page.save()

        messages.success(
            request,
            "Homepage settings updated successfully."
        )

    return redirect("home_management")

def update_home_visibility(request):
    """
    Update homepage section visibility settings only.
    """

    home_page = HomePage.objects.first()

    if not home_page:
        home_page = HomePage.objects.create()

    if request.method == "POST":

        home_page.hero_is_active = (
            request.POST.get("hero_is_active") == "on"
        )

        home_page.categories_is_active = (
            request.POST.get("categories_is_active") == "on"
        )

        home_page.featured_is_active = (
            request.POST.get("featured_is_active") == "on"
        )

        home_page.new_arrivals_is_active = (
            request.POST.get("new_arrivals_is_active") == "on"
        )

        home_page.second_hero_is_active = (
            request.POST.get("second_hero_is_active") == "on"
        )

        home_page.save()

        messages.success(
            request,
            "Homepage section visibility updated successfully."
        )

    return redirect("home_management")


def update_second_hero(request):
    """
    Update second hero image only.
    """

    home_page = HomePage.objects.first()

    if not home_page:
        home_page = HomePage.objects.create()

    if request.method == "POST":

        second_hero_image = request.FILES.get(
            "second_hero_image"
        )

        if second_hero_image:
            home_page.second_hero_image = second_hero_image

        home_page.save()

        messages.success(
            request,
            "Second hero updated successfully."
        )

    return redirect("home_management")


def add_home_slide(request):
    """
    Add a new homepage hero slide.
    """

    home_page = HomePage.objects.first()

    if not home_page:
        home_page = HomePage.objects.create()

    if request.method == "POST":

        desktop_image = request.FILES.get("desktop_image")
        mobile_image = request.FILES.get("mobile_image")

        alt_text = request.POST.get(
            "alt_text",
            ""
        ).strip()

        display_order = request.POST.get(
            "display_order",
            "0"
        )

        try:
            display_order = int(display_order)
        except (TypeError, ValueError):
            display_order = 0

        # ==========================================
        # DESKTOP IMAGE REQUIRED
        # ==========================================

        if not desktop_image:
            messages.error(
                request,
                "Desktop hero image is required."
            )

            return redirect("home_management")

        # ==========================================
        # CREATE SLIDE
        # ==========================================

        try:

            slide = HomeHeroSlide(
                home_page=home_page,
                desktop_image=desktop_image,
                mobile_image=mobile_image,
                alt_text=alt_text,
                display_order=display_order,
                is_active=True,
            )

            # Run model validation
            slide.full_clean()

            slide.save()

            messages.success(
                request,
                "Hero slide added successfully."
            )

        except ValidationError as error:

            messages.error(
                request,
                error.messages[0]
            )

    return redirect("home_management")



def update_home_slide(request, slide_id):
    """
    Update an existing homepage hero slide.
    """

    slide = get_object_or_404(
        HomeHeroSlide,
        id=slide_id
    )

    if request.method == "POST":

        desktop_image = request.FILES.get("desktop_image")
        mobile_image = request.FILES.get("mobile_image")

        # ==========================================
        # TEXT DATA
        # ==========================================

        slide.alt_text = request.POST.get(
            "alt_text",
            ""
        ).strip()

        # ==========================================
        # DISPLAY ORDER
        # ==========================================

        display_order = request.POST.get(
            "display_order",
            slide.display_order
        )

        try:
            slide.display_order = int(display_order)
        except (TypeError, ValueError):
            slide.display_order = 0

        # ==========================================
        # ACTIVE / INACTIVE
        # ==========================================

        slide.is_active = (
            request.POST.get("is_active") == "on"
        )

        # ==========================================
        # REPLACE DESKTOP IMAGE
        # ==========================================

        if desktop_image:
            slide.desktop_image = desktop_image

        # ==========================================
        # REPLACE MOBILE IMAGE
        # ==========================================

        if mobile_image:
            slide.mobile_image = mobile_image

        # ==========================================
        # VALIDATE
        # ==========================================

        try:

            slide.full_clean()

            slide.save()

            messages.success(
                request,
                "Hero slide updated successfully."
            )

        except ValidationError as error:

            messages.error(
                request,
                error.messages[0]
            )

    return redirect("home_management")



def delete_home_slide(request, slide_id):
    """
    Delete an existing homepage hero slide.
    """

    slide = get_object_or_404(
        HomeHeroSlide,
        id=slide_id
    )

    if request.method == "POST":

        slide.delete()

        messages.success(
            request,
            "Hero slide deleted successfully."
        )

    return redirect("home_management")