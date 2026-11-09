
from .permissions import (
    get_admin_role,
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


def admin_permissions(request):
    """Provide role-based visibility flags to admin templates."""

    user = request.user
    role = get_admin_role(user)

    permissions = {
        "dashboard": role is not None,
        "products": can_manage_products(user),
        "categories": can_manage_products(user),
        "orders": can_view_orders(user),
        "customers": can_view_customers(user),
        "inventory": can_manage_inventory(user),
        "coupons": can_manage_coupons(user),
        "reviews": can_view_reviews(user),
        "reports": can_view_reports(user),
        "settings": can_manage_general_settings(user),
        "store_content": can_manage_store_content(user),
        "admin_users": role == "Owner",
        "logout": role is not None,
    }

    return {
        "admin_role": role,
        "admin_permissions": permissions,
    }
