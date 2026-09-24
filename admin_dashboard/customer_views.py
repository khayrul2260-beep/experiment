from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import *
from experiment1.models import *
from django.contrib.auth import get_user_model
from django.db.models import Count


def orders_page(request):

    orders = (
        Order.objects
        .select_related("customer")
        .prefetch_related(
            "items",
            "return_exchange_requests",
        )
        .order_by("-created_at")
    )

    order_counts = orders.aggregate(
        total=Count("id"),
        pending=Count(
            "id",
            filter=models.Q(status="Pending")
        ),
        confirmed=Count(
            "id",
            filter=models.Q(status="Confirmed")
        ),
        processing=Count(
            "id",
            filter=models.Q(status="Processing")
        ),
        shipped=Count(
            "id",
            filter=models.Q(status="Shipped")
        ),
        delivered=Count(
            "id",
            filter=models.Q(status="Delivered")
        ),
        cancelled=Count(
            "id",
            filter=models.Q(status="Cancelled")
        ),
    )

    return render(
        request,
        "admin_dashboard/orders.html",
        {
            "page_title": "Orders",
            "orders": orders,
            "order_counts": order_counts,
        }
    )


def order_details_page(request, order_number):

    order = get_object_or_404(
        Order.objects
        .select_related("customer")
        .prefetch_related(
            "items",
            "return_exchange_requests",
        ),
        order_number=order_number,
    )

    return_requests = order.return_exchange_requests.all()

    context = {
        "page_title": "Order Details",
        "order": order,
        "return_requests": return_requests,
    }

    return render(
        request,
        "admin_dashboard/order_details.html",
        context
    )

def update_order_status(request, order_number):

    if request.method != "POST":
        return redirect(
            "admin_order_details",
            order_number=order_number
        )

    order = get_object_or_404(
        Order,
        order_number=order_number
    )

    new_status = request.POST.get("status")

    valid_statuses = [
        choice[0]
        for choice in Order.STATUS_CHOICES
    ]

    if new_status not in valid_statuses:
        messages.error(
            request,
            "Invalid order status."
        )

        return redirect(
            "admin_order_details",
            order_number=order.order_number
        )

    if order.status == new_status:
        messages.info(
            request,
            "Order status is already set to this status."
        )

        return redirect(
            "admin_order_details",
            order_number=order.order_number
        )

    old_status = order.status

    order.status = new_status

    order.save(
        update_fields=[
            "status",
            "updated_at"
        ]
    )

    messages.success(
        request,
        f"Order status updated from {old_status} to {new_status}."
    )

    return redirect(
        "admin_order_details",
        order_number=order.order_number
    )

User = get_user_model()

def customers_page(request):

    # =========================================================
    # REGISTERED CUSTOMERS
    # =========================================================

    registered_customers = (
        User.objects
        .filter(is_staff=False)
        .prefetch_related(
            "orders__items"
        )
        .order_by("-date_joined")
    )


    registered_customer_data = []

    for customer in registered_customers:

        customer_orders = list(
            customer.orders.all()
        )

        valid_orders = [
            order
            for order in customer_orders
            if order.status != "Cancelled"
        ]

        total_orders = len(valid_orders)

        total_items = sum(
            item.quantity
            for order in valid_orders
            for item in order.items.all()
        )

        total_spent = sum(
            order.total_amount
            for order in valid_orders
            if order.status == "Delivered"
        )

        last_order = max(
            customer_orders,
            key=lambda order: order.created_at,
            default=None
        )


        registered_customer_data.append({
            "id": customer.id,
            "name": (
                customer.get_full_name()
                or customer.username
            ),
            "username": customer.username,
            "email": customer.email,
            "phone": getattr(customer, "phone", ""),
            "profile_image": customer.profile_image,
            "type": "REGISTERED",

            "total_orders": total_orders,
            "total_items": total_items,
            "total_spent": total_spent,

            "date_joined": customer.date_joined,
            "last_order": (
                last_order.created_at
                if last_order
                else None
            ),

            "is_active": customer.is_active,
            "status": (
                "Active"
                if customer.is_active
                else "Inactive"
            ),
        })


    # =========================================================
    # GUEST CUSTOMERS
    # =========================================================

    guest_orders = (
        Order.objects
        .filter(
            customer__isnull=True
        )
        .prefetch_related("items")
        .order_by("-created_at")
    )


    guest_groups = {}


    for order in guest_orders:

        # -----------------------------------------------------
        # PHONE PRIMARY IDENTIFIER
        # -----------------------------------------------------

        phone = "".join(
            character
            for character in (order.phone or "")
            if character.isdigit()
        )


        # -----------------------------------------------------
        # EMAIL FALLBACK
        # -----------------------------------------------------

        email = (
            (order.email or "")
            .strip()
            .lower()
        )


        if phone:

            guest_key = f"phone:{phone}"

        elif email:

            guest_key = f"email:{email}"

        else:

            # No phone/email available.
            # Keep this order as a separate guest.
            guest_key = f"order:{order.id}"


        # -----------------------------------------------------
        # CREATE GUEST GROUP
        # -----------------------------------------------------

        if guest_key not in guest_groups:

            guest_groups[guest_key] = {
                "id": guest_key,

                "name": order.full_name,

                "username": "",

                "email": order.email,

                "phone": order.phone,

                "profile_image": None,

                "type": "GUEST",

                "orders": [],

                "total_orders": 0,

                "total_items": 0,

                "total_spent": 0,

                "date_joined": order.created_at,

                "last_order": order.created_at,

                "is_active": True,

                "status": "Guest",
            }


        guest = guest_groups[guest_key]


        # -----------------------------------------------------
        # ORDER COUNT
        # -----------------------------------------------------

        guest["orders"].append(
            order.id
        )

        guest["total_orders"] += 1


        # -----------------------------------------------------
        # ITEM QUANTITY
        # -----------------------------------------------------

        if order.status != "Cancelled":

            guest["total_items"] += sum(
                item.quantity
                for item in order.items.all()
            )


        # -----------------------------------------------------
        # SPENT
        # -----------------------------------------------------

        if order.status == "Delivered":

            guest["total_spent"] += (
                order.total_amount
            )


        # -----------------------------------------------------
        # FIRST ORDER
        # -----------------------------------------------------

        if order.created_at < guest["date_joined"]:

            guest["date_joined"] = (
                order.created_at
            )


        # -----------------------------------------------------
        # LAST ORDER
        # -----------------------------------------------------

        if order.created_at > guest["last_order"]:

            guest["last_order"] = (
                order.created_at
            )


    guest_customer_data = list(
        guest_groups.values()
    )


    # =========================================================
    # COMBINE REGISTERED + GUEST
    # =========================================================

    customers = (
        registered_customer_data
        + guest_customer_data
    )


    # =========================================================
    # PURCHASE RANKING
    #
    # Highest total item quantity first
    # =========================================================

    customers.sort(
        key=lambda customer: (
            customer["total_items"],
            customer["total_orders"],
        ),
        reverse=True
    )


    # =========================================================
    # CUSTOMER COUNTS
    # =========================================================

    total_registered = len(
        registered_customer_data
    )

    total_guest = len(
        guest_customer_data
    )

    total_customers = (
        total_registered
        + total_guest
    )


    total_active = sum(
        1
        for customer in registered_customer_data
        if customer["is_active"]
    )


    total_inactive = sum(
        1
        for customer in registered_customer_data
        if not customer["is_active"]
    )


    # =========================================================
    # CONTEXT
    # =========================================================

    context = {

        "page_title": "Customers",

        "customers": customers,

        "customer_counts": {

            "total": total_customers,

            "registered": total_registered,

            "guest": total_guest,

            "active": total_active,

            "inactive": total_inactive,

        },

    }


    # =========================================================
    # RENDER
    # =========================================================

    return render(
        request,
        "admin_dashboard/customers.html",
        context
    )



def inventory_page(request):

    return render(request, 'admin_dashboard/inventory.html', { "page_title": "Inventory" })  




def coupons_page(request):

    return render(request, 'admin_dashboard/coupons.html', { "page_title": "Coupons" })   



def reviews_page(request):

    return render(request, 'admin_dashboard/reviews.html', { "page_title": "Reviews" })    




def reports_page(request):

    return render(request, 'admin_dashboard/reports.html', { "page_title": "Reports" })




