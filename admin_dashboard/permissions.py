"""
NAFI Admin Dashboard

Centralized role-based access control (RBAC).
Roles: Owner, Manager, Support, Warehouse.
"""

OWNER_ROLE = "Owner"
MANAGER_ROLE = "Manager"
SUPPORT_ROLE = "Support"
WAREHOUSE_ROLE = "Warehouse"

ADMIN_ROLES = {
    OWNER_ROLE,
    MANAGER_ROLE,
    SUPPORT_ROLE,
    WAREHOUSE_ROLE,
}

def get_admin_role(user):
    """
    Return the user's NAFI admin role.
    Superusers are treated as Owner.
    """

    if not user.is_authenticated or not user.is_active or not user.is_staff:
        return None

    if user.is_superuser:
        return OWNER_ROLE

    for role in (MANAGER_ROLE, SUPPORT_ROLE, WAREHOUSE_ROLE):
        if user.groups.filter(name=role).exists():
            return role

    return None

# Roles allowed to perform sensitive administrative actions.

ALL_ADMIN_ROLES = frozenset({
    OWNER_ROLE,
    MANAGER_ROLE,
    SUPPORT_ROLE,
    WAREHOUSE_ROLE,
})

MANAGEMENT_ROLES = frozenset({
    OWNER_ROLE,
    MANAGER_ROLE,
})

CUSTOMER_SUPPORT_ROLES = frozenset({
    OWNER_ROLE,
    MANAGER_ROLE,
    SUPPORT_ROLE,
})

INVENTORY_ROLES = frozenset({
    OWNER_ROLE,
    MANAGER_ROLE,
    WAREHOUSE_ROLE,
})

OWNER_ONLY_ROLES = frozenset({
    OWNER_ROLE,
})

def can_update_payment_status(user):
    """
    Only Owner and Manager can update payment status.
    """
    return get_admin_role(user) in MANAGEMENT_ROLES


def can_update_order_status(user):
    """Owner, Manager and Support can update order status."""
    return get_admin_role(user) in CUSTOMER_SUPPORT_ROLES

def can_manage_return_exchange(user):
    """Only Owner and Manager can approve, reject or complete returns/exchanges."""
    return get_admin_role(user) in MANAGEMENT_ROLES

def can_manage_products(user):
    """Only Owner and Manager can manage products and categories."""
    return get_admin_role(user) in MANAGEMENT_ROLES

def can_manage_inventory(user):
    """Owner, Manager and Warehouse can manage inventory."""
    return get_admin_role(user) in INVENTORY_ROLES

def can_manage_coupons(user):
    """Only Owner and Manager can access coupon management."""
    return get_admin_role(user) in MANAGEMENT_ROLES

def can_view_orders(user):
    """Only Owner, Manager and Support can view orders."""
    return get_admin_role(user) in CUSTOMER_SUPPORT_ROLES

def can_view_customers(user):
    """Owner, Manager and Support can view customer information."""
    return get_admin_role(user) in CUSTOMER_SUPPORT_ROLES

def can_view_reviews(user):
    """Owner, Manager and Support can access reviews."""
    return get_admin_role(user) in CUSTOMER_SUPPORT_ROLES

def can_view_reports(user):
    """Only Owner and Manager can access reports."""
    return get_admin_role(user) in MANAGEMENT_ROLES


def can_manage_store_content(user):
    """
    Owner and Manager can manage Homepage,
    About, Contact and Delivery Settings.
    """
    return get_admin_role(user) in MANAGEMENT_ROLES


def can_manage_general_settings(user):
    """
    Only Owner can access General Settings.
    """
    return get_admin_role(user) in OWNER_ONLY_ROLES
