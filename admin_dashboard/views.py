from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from .models import *
from django.db.models import Q
from .forms import CategoryForm



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
    ).order_by('name')

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

        price = request.POST.get("price")

        discount_price = (
            request.POST.get("discount_price")
            or None
        )

        image = request.FILES.get("image")

        additional_images = request.FILES.getlist(
            "additional_images"
        )
        
        is_available = (
            "is_available" in request.POST
        )

        is_featured = (
            "is_featured" in request.POST
        )

        category_id = request.POST.get(
            "category"
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
        # IMAGE VALIDATION
        # ==========================================

        if image is None:

            messages.error(
                request,
                "Please upload an image."
            )

            return redirect(
                "add_product_page"
            )


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
        # CREATE PRODUCT
        # ==========================================

        product = ProductsModel.objects.create(

            name=product_name,

            description=description,

            price=price,

            discount_price=discount_price,

            stock=total_stock,

            image=image,

            is_available=is_available,

            is_featured=is_featured,

            category_id=category_id,
        )
        for image_file in additional_images:
        
            ProductImage.objects.create(
                product=product,
                image=image_file
            )


        # ==========================================
        # CREATE PRODUCT SIZE RECORDS
        # ==========================================

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

    # ==========================================
    # GET PRODUCT
    # ==========================================

    product = get_object_or_404(
        ProductsModel,
        id=id
    )


    # ==========================================
    # GET CATEGORIES
    # ==========================================

    categories = Category.objects.filter(
        Q(is_active=True) |
        Q(id=product.category_id)
    ).order_by('name')


    # ==========================================
    # GET EXISTING SIZES
    # ==========================================

    existing_sizes = {
        item.size: item
        for item in product.sizes.all()
    }


    # ==========================================
    # GET EXISTING ADDITIONAL IMAGES
    # ==========================================

    additional_images = product.images.all()


    # ==========================================
    # POST
    # ==========================================

    if request.method == "POST":

        product_name = request.POST.get(
            "product_name",
            ""
        ).strip()

        description = request.POST.get(
            "description",
            ""
        ).strip()

        price = request.POST.get("price")

        discount_price = (
            request.POST.get("discount_price")
            or None
        )

        # Main product image
        image = request.FILES.get("image")

        # Additional product images
        additional_images_upload = request.FILES.getlist(
            "additional_images"
        )

        is_available = (
            "is_available" in request.POST
        )

        is_featured = (
            "is_featured" in request.POST
        )

        category_id = request.POST.get(
            "category"
        )


        # ==========================================
        # SIZE-WISE STOCK
        # ==========================================

        size_stock = {}

        for size in ["M", "L", "XL", "XXL"]:

            size_selected = (
                f"size_{size}" in request.POST
            )

            if not size_selected:
                continue


            stock_value = request.POST.get(
                f"stock_{size}",
                "0"
            )


            try:

                stock_value = int(
                    stock_value or 0
                )

            except (ValueError, TypeError):

                stock_value = 0


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


        # ==========================================
        # SIZE VALIDATION
        # ==========================================

        if not size_stock:

            messages.error(
                request,
                "Please select at least one size and enter its stock."
            )

            return redirect(
                "edit_product_page",
                id=product.id
            )


        # ==========================================
        # TOTAL STOCK
        # ==========================================

        total_stock = sum(
            size_stock.values()
        )


        # ==========================================
        # UPDATE PRODUCT
        # ==========================================

        product.name = product_name

        product.description = description

        product.price = price

        product.discount_price = discount_price

        product.stock = total_stock

        product.category_id = category_id

        product.is_available = is_available

        product.is_featured = is_featured


        # ==========================================
        # UPDATE MAIN IMAGE
        # ==========================================

        if image:

            product.image = image


        # ==========================================
        # SAVE PRODUCT
        # ==========================================

        product.save()


        # ==========================================
        # SAVE ADDITIONAL IMAGES
        # ==========================================

        for image_file in additional_images_upload:

            ProductImage.objects.create(

                product=product,

                image=image_file

            )


        # ==========================================
        # UPDATE PRODUCT SIZES
        # ==========================================

        for size in ["M", "L", "XL", "XXL"]:

            if size in size_stock:

                ProductSize.objects.update_or_create(

                    product=product,

                    size=size,

                    defaults={
                        "stock": size_stock[size],
                        "is_available": True,
                    }

                )

            else:

                ProductSize.objects.filter(
                    product=product,
                    size=size
                ).delete()


        # ==========================================
        # SAVE ACTION
        # ==========================================

        action = request.POST.get(
            "save_action"
        )


        if action == "save":

            messages.success(
                request,
                "Product updated successfully."
            )

            return redirect(
                "products_page"
            )


        elif action == "save_add":

            messages.success(
                request,
                "Product updated successfully."
            )

            return redirect(
                "add_product_page"
            )


        elif action == "save_edit":

            messages.success(
                request,
                "Product updated successfully."
            )

            return redirect(
                "edit_product_page",
                id=product.id
            )


        else:

            return redirect(
                "products_page"
            )


    # ==========================================
    # CONTEXT
    # ==========================================

    context = {

        "product": product,

        "page_title": "Products",

        "categories": categories,

        "existing_sizes": existing_sizes,

        "additional_images": additional_images,

    }


    # ==========================================
    # RENDER
    # ==========================================

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

