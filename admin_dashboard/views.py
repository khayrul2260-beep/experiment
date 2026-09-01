from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from .models import *
from django.db.models import Q
from .forms import CategoryForm
from django.db import transaction



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

