
from functools import wraps
from django.urls import path
from django.http import Http404
from django.shortcuts import redirect
from .permissions import (
    get_admin_role,
    can_update_payment_status,
    can_update_order_status,
    can_manage_return_exchange,
    can_manage_products,
    can_manage_inventory,
    can_manage_coupons,
    can_view_orders,
    can_view_customers,
    can_view_reviews,
    can_view_reports,
    can_manage_store_content,
    can_manage_general_settings,
)

def admin_access_required(view_func):
    @wraps(view_func)
    def protected_view(request, *args, **kwargs):
        user = request.user
        if get_admin_role(user) is None:
            raise Http404("Page not found.")

        if (
            request.session.get("admin_verified") is not True
            or request.session.get("admin_verified_user_id") != user.pk
            or request.session.get("admin_verified_auth_hash")
            != user.get_session_auth_hash()
        ):
            return redirect("admin_password_verify")

        return view_func(request, *args, **kwargs)

    return protected_view

def owner_access_required(view_func):
    @wraps(view_func)
    def protected_view(request, *args, **kwargs):

        user = request.user

        # Owner authorization
        if (
            not user.is_authenticated
            or not user.is_active
            or not user.is_staff
            or not user.is_superuser
        ):
            raise Http404("Page not found.")

        # Password verification
        if (
            request.session.get("admin_verified") is not True
            or request.session.get("admin_verified_user_id") != user.pk
            or request.session.get("admin_verified_auth_hash")
            != user.get_session_auth_hash()
        ):
            return redirect("admin_password_verify")

        return view_func(request, *args, **kwargs)

    return protected_view

def admin_session_verification_required(view_func):
    @wraps(view_func)
    def protected_view(request, *args, **kwargs):

        user = request.user

        # Only authorized Admin users
        if get_admin_role(user) is None:
            raise Http404("Page not found.")

        # Verify current session
        if (
            request.session.get("admin_verified") is not True
            or request.session.get("admin_verified_user_id") != user.pk
            or request.session.get("admin_verified_auth_hash")
            != user.get_session_auth_hash()
        ):
            return redirect("admin_password_verify")

        return view_func(request, *args, **kwargs)

    return protected_view

def payment_status_access_required(view_func):
    @wraps(view_func)
    def protected_view(request, *args, **kwargs):
        if not can_update_payment_status(request.user):
            raise Http404("Page not found.")

        return view_func(request, *args, **kwargs)

    return protected_view

def order_status_access_required(view_func):
    @wraps(view_func)
    def protected_view(request, *args, **kwargs):
        if not can_update_order_status(request.user):
            raise Http404("Page not found.")

        return view_func(request, *args, **kwargs)

    return protected_view

def return_exchange_access_required(view_func):
    @wraps(view_func)
    def protected_view(request, *args, **kwargs):
        if not can_manage_return_exchange(request.user):
            raise Http404("Page not found.")

        return view_func(request, *args, **kwargs)

    return protected_view

def product_management_access_required(view_func):
    @wraps(view_func)
    def protected_view(request, *args, **kwargs):
        if not can_manage_products(request.user):
            raise Http404("Page not found.")

        return view_func(request, *args, **kwargs)

    return protected_view


def inventory_access_required(view_func):
    @wraps(view_func)
    def protected_view(request, *args, **kwargs):
        if not can_manage_inventory(request.user):
            raise Http404("Page not found.")

        return view_func(request, *args, **kwargs)

    return protected_view

def coupon_access_required(view_func):
    @wraps(view_func)
    def protected_view(request, *args, **kwargs):
        if not can_manage_coupons(request.user):
            raise Http404("Page not found.")

        return view_func(request, *args, **kwargs)

    return protected_view

def order_view_access_required(view_func):
    @wraps(view_func)
    def protected_view(request, *args, **kwargs):
        if not can_view_orders(request.user):
            raise Http404("Page not found.")

        return view_func(request, *args, **kwargs)

    return protected_view

def customer_access_required(view_func):
    @wraps(view_func)
    def protected_view(request, *args, **kwargs):
        if not can_view_customers(request.user):
            raise Http404("Page not found.")

        return view_func(request, *args, **kwargs)

    return protected_view

def reviews_access_required(view_func):
    @wraps(view_func)
    def protected_view(request, *args, **kwargs):
        if not can_view_reviews(request.user):
            raise Http404("Page not found.")

        return view_func(request, *args, **kwargs)

    return protected_view


def reports_access_required(view_func):
    @wraps(view_func)
    def protected_view(request, *args, **kwargs):
        if not can_view_reports(request.user):
            raise Http404("Page not found.")

        return view_func(request, *args, **kwargs)

    return protected_view


def store_content_access_required(view_func):
    @wraps(view_func)
    def protected_view(request, *args, **kwargs):
        if not can_manage_store_content(request.user):
            raise Http404("Page not found.")

        return view_func(request, *args, **kwargs)

    return protected_view


def general_settings_access_required(view_func):
    @wraps(view_func)
    def protected_view(request, *args, **kwargs):
        if not can_manage_general_settings(request.user):
            raise Http404("Page not found.")

        return view_func(request, *args, **kwargs)

    return protected_view


from .views import *
from .contact_views import *
from .customer_views import *


urlpatterns = [
    path("", dashboard_page, name="dashboard_page"),
    path('products/', products_page, name='products_page'),
    path('categories/', categories_page, name='categories_page'),

    path('orders/', orders_page, name='orders_page'),
    path("orders/<str:order_number>/", order_details_page, name="admin_order_details"),
    path("orders/<str:order_number>/update-status/", update_order_status, name="update_order_status"),
    path("orders/<str:order_number>/update-payment-status/", update_payment_status, name="update_payment_status"),
    path("orders/return-exchange/<int:request_id>/approve/",approve_return_exchange,name="approve_return_exchange"),
    path("orders/return-exchange/<int:request_id>/reject/",reject_return_exchange,name="reject_return_exchange"),
    path("orders/return-exchange/<int:request_id>/complete/",complete_return_exchange,name="complete_return_exchange"),

    path('customers/', customers_page, name='customers_page'),
    path("customers/<str:customer_id>/", customer_details_page, name="customer_details"),

    path('inventory/', inventory_page, name='inventory_page'),
    path('inventory/update-stock/', update_inventory_stock, name='update_inventory_stock'),

    path('coupons/', coupons_page, name='coupons_page'),
    path('coupons/create/',create_coupon,name='create_coupon'),
    path('coupons/<int:coupon_id>/update/', update_coupon, name='update_coupon'),
    path('coupons/<int:coupon_id>/toggle/', toggle_coupon, name='toggle_coupon'),
    path('coupons/<int:coupon_id>/delete/', delete_coupon, name='delete_coupon'),

    path('reviews/', reviews_page, name='reviews_page'),
    path('reports/', reports_page, name='reports_page'),

    path('settings/', settings_page, name='settings_page'),
    path('settings/delivery/', delivery_settings_page, name='delivery_settings_page'),
    path('settings/home/', home_management, name='home_management'),
    path('settings/home/update/', update_home_page, name='update_home_page'),
    path("settings/home/visibility/update/", update_home_visibility, name="update_home_visibility"),
    path("settings/home/second-hero/update/", update_second_hero, name="update_second_hero"),
    path('settings/home/slide/add/', add_home_slide, name='add_home_slide'),
    path('settings/home/slide/<int:slide_id>/update/', update_home_slide, name='update_home_slide'),
    path('settings/home/slide/<int:slide_id>/delete/', delete_home_slide, name='delete_home_slide'),
    path("settings/about/", about_management, name="about_management"),
    path("settings/about/update/", update_about_page, name="update_about_page"),
    path("settings/about/value/add/", add_about_value, name="add_about_value"),
    path("settings/about/value/<int:value_id>/delete/", delete_about_value, name="delete_about_value"),
    path("settings/about/quality/add/", add_about_quality, name="add_about_quality"),
    path("settings/about/quality/<int:quality_id>/delete/", delete_about_quality, name="delete_about_quality"),
    path("settings/about/journey/add/", add_about_journey, name="add_about_journey"),
    path("settings/about/journey/<int:journey_id>/delete/", delete_about_journey, name="delete_about_journey"),
    path("settings/about/value/<int:value_id>/update/", update_about_value, name="update_about_value"),
    path("settings/about/quality/<int:quality_id>/update/", update_about_quality, name="update_about_quality"),
    path("settings/about/journey/<int:journey_id>/update/", update_about_journey, name="update_about_journey"),

    path("settings/contact/", contact_management, name="contact_management"),
    path("settings/contact/service/add/", add_contact_service, name="add_contact_service"),
    path("settings/contact/service/<int:service_id>/update/", update_contact_service, name="update_contact_service"),
    path("settings/contact/service/<int:service_id>/delete/", delete_contact_service, name="delete_contact_service"),
    path("settings/contact/faq/add/", add_contact_faq, name="add_contact_faq"),
    path("settings/contact/faq/<int:faq_id>/update/", update_contact_faq, name="update_contact_faq"),
    path("settings/contact/faq/<int:faq_id>/delete/", delete_contact_faq, name="delete_contact_faq"),
    path("settings/contact/social/add/",add_contact_social_link,name="add_contact_social_link"),
    path("settings/contact/social/<int:social_id>/update/",update_contact_social_link,name="update_contact_social_link"),
    path("settings/contact/social/<int:social_id>/delete/",delete_contact_social_link,name="delete_contact_social_link"),

    path("admin_users/invitation/create/", create_admin_invitation, name="create_admin_invitation"),
    path('admin_users/', admin_users_page, name='admin_users_page'),
    path("admin_users/<int:user_id>/promote/", promote_customer_to_staff, name="promote_customer_to_staff"),
    path("admin_users/<int:user_id>/role/", change_staff_role, name="change_staff_role"),
    path("admin_users/<int:user_id>/revoke/", revoke_staff_access, name="revoke_staff_access"),
    path('logout/', logout_page, name='logout_page'),
    path('hidden_sidebar/', hidden_sidebar_page, name='hidden_sidebar_page'),
    path("product/add/", add_product_page, name="add_product_page"),
    path("product/edit/<int:id>/", edit_product_page, name="edit_product_page"),
    path("delete/<int:id>/", delete_product_page, name="delete_product_page"),
    path("categories/add/", add_category, name='add_category'),
    path("categories/delete/<int:id>/", delete_category, name="delete_category"),
    path("category/edit/<int:id>/", edit_category, name="edit_category"),
]


# Protect every custom admin dashboard endpoint.
# Guest and non-staff users receive HTTP 404.
# Admin Users is restricted to the Owner (superuser).

RETURN_EXCHANGE_ACTIONS = {
    "approve_return_exchange",
    "reject_return_exchange",
    "complete_return_exchange",
}

PRODUCT_MANAGEMENT_ACTIONS = {
    "products_page",
    "categories_page",
    "add_product_page",
    "edit_product_page",
    "delete_product_page",
    "add_category",
    "edit_category",
    "delete_category",
}

INVENTORY_ACTIONS = {
    "inventory_page",
    "update_inventory_stock",
}

COUPON_ACTIONS = {
    "coupons_page",
    "create_coupon",
    "update_coupon",
    "toggle_coupon",
    "delete_coupon",
}

CUSTOMER_ACTIONS = {
    "customers_page",
    "customer_details",
}


STORE_CONTENT_ACTIONS = {
    "delivery_settings_page",
    "home_management",
    "update_home_page",
    "update_home_visibility",
    "update_second_hero",
    "add_home_slide",
    "update_home_slide",
    "delete_home_slide",
    "about_management",
    "update_about_page",
    "add_about_value",
    "delete_about_value",
    "add_about_quality",
    "delete_about_quality",
    "add_about_journey",
    "delete_about_journey",
    "update_about_value",
    "update_about_quality",
    "update_about_journey",
    "contact_management",
    "add_contact_service",
    "update_contact_service",
    "delete_contact_service",
    "add_contact_faq",
    "update_contact_faq",
    "delete_contact_faq",
    "add_contact_social_link",
    "update_contact_social_link",
    "delete_contact_social_link",
}

for pattern in urlpatterns:
    if pattern.name in {
        "admin_users_page",
        "create_admin_invitation",
        "promote_customer_to_staff",
        "change_staff_role",
        "revoke_staff_access",
    }:
        pattern.callback = owner_access_required(pattern.callback)

    elif pattern.name == "update_payment_status":
        pattern.callback = payment_status_access_required(pattern.callback)

    elif pattern.name == "update_order_status":
        pattern.callback = order_status_access_required(pattern.callback)

    elif pattern.name in RETURN_EXCHANGE_ACTIONS:
        pattern.callback = return_exchange_access_required(pattern.callback)

    elif pattern.name in PRODUCT_MANAGEMENT_ACTIONS:
        pattern.callback = product_management_access_required(pattern.callback)

    elif pattern.name in INVENTORY_ACTIONS:
        pattern.callback = inventory_access_required(pattern.callback)

    elif pattern.name in COUPON_ACTIONS:
        pattern.callback = coupon_access_required(pattern.callback)

    elif pattern.name in {"orders_page", "admin_order_details"}:
        pattern.callback = order_view_access_required(pattern.callback)

    elif pattern.name in CUSTOMER_ACTIONS:
        pattern.callback = customer_access_required(pattern.callback)

    elif pattern.name == "reviews_page":
        pattern.callback = reviews_access_required(pattern.callback)

    elif pattern.name == "reports_page":
        pattern.callback = reports_access_required(pattern.callback)

    elif pattern.name == "settings_page":
        pattern.callback = general_settings_access_required(pattern.callback)

    elif pattern.name in STORE_CONTENT_ACTIONS:
        pattern.callback = store_content_access_required(pattern.callback)

    else:
        pattern.callback = admin_access_required(pattern.callback)

# Enforce password verification on every admin URL
for pattern in urlpatterns:
    pattern.callback = admin_session_verification_required(
        pattern.callback
    )