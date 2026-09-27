from decimal import Decimal, ROUND_HALF_UP, InvalidOperation

from django.utils import timezone
from django.utils.dateparse import parse_datetime

from admin_dashboard.models import Coupon


def validate_coupon(code, subtotal, coupon=None):
    """
    Validate a coupon against the current order subtotal.

    Args:
        code: Coupon code.
        subtotal: Current order subtotal.
        coupon: Optional Coupon instance.
                If provided, database lookup is skipped.

    Returns:
        {
            "valid": True/False,
            "coupon": Coupon | None,
            "discount": Decimal,
            "message": str,
        }
    """

    if not code:
        return {
            "valid": False,
            "coupon": None,
            "discount": Decimal("0.00"),
            "message": "Please enter a coupon code.",
        }

    try:
        subtotal = Decimal(str(subtotal))
    except (InvalidOperation, ValueError, TypeError):
        return {
            "valid": False,
            "coupon": None,
            "discount": Decimal("0.00"),
            "message": "Invalid order amount.",
        }

    if subtotal < Decimal("0.00"):
        return {
            "valid": False,
            "coupon": None,
            "discount": Decimal("0.00"),
            "message": "Invalid order amount.",
        }

    normalized_code = str(code).strip().upper()

    # Use supplied coupon when available.
    # Otherwise fetch it from the database.
    if coupon is None:
        try:
            coupon = Coupon.objects.get(
                code__iexact=normalized_code
            )
        except Coupon.DoesNotExist:
            return {
                "valid": False,
                "coupon": None,
                "discount": Decimal("0.00"),
                "message": "Invalid coupon code.",
            }

    if not coupon.is_active:
        return {
            "valid": False,
            "coupon": coupon,
            "discount": Decimal("0.00"),
            "message": "This coupon is currently inactive.",
        }

    now = timezone.now()

    if now < coupon.start_date:
        return {
            "valid": False,
            "coupon": coupon,
            "discount": Decimal("0.00"),
            "message": "This coupon is not active yet.",
        }

    if now > coupon.expiry_date:
        return {
            "valid": False,
            "coupon": coupon,
            "discount": Decimal("0.00"),
            "message": "This coupon has expired.",
        }

    if (
        coupon.usage_limit is not None
        and coupon.used_count >= coupon.usage_limit
    ):
        return {
            "valid": False,
            "coupon": coupon,
            "discount": Decimal("0.00"),
            "message": "This coupon usage limit has been reached.",
        }

    if subtotal < coupon.minimum_order_amount:
        return {
            "valid": False,
            "coupon": coupon,
            "discount": Decimal("0.00"),
            "message": (
                f"Minimum order amount is "
                f"৳{coupon.minimum_order_amount:.2f}."
            ),
        }

    discount = Decimal("0.00")

    # Percentage discount
    if coupon.discount_type == "percentage":

        if coupon.discount_value > Decimal("100"):
            return {
                "valid": False,
                "coupon": coupon,
                "discount": Decimal("0.00"),
                "message": (
                    "Invalid percentage discount configuration."
                ),
            }

        discount = (
            subtotal
            * coupon.discount_value
            / Decimal("100")
        )

        # Apply maximum discount limit
        if coupon.maximum_discount is not None:
            discount = min(
                discount,
                coupon.maximum_discount
            )

    # Fixed amount discount
    elif coupon.discount_type == "fixed":

        discount = coupon.discount_value

    else:
        return {
            "valid": False,
            "coupon": coupon,
            "discount": Decimal("0.00"),
            "message": "Invalid coupon discount type.",
        }

    # Discount can never be greater than subtotal
    discount = min(
        discount,
        subtotal
    )

    # Keep money value at 2 decimal places
    discount = discount.quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP
    )

    return {
        "valid": True,
        "coupon": coupon,
        "discount": discount,
        "message": "Coupon applied successfully.",
    }


def validate_coupon_data(data, coupon=None):
    """
    Validate coupon data before creating or updating a Coupon.

    Args:
        data: POST data / dictionary containing coupon information.
        coupon: Existing Coupon instance during update.
                None when creating a new coupon.

    Returns:
        {
            "valid": True/False,
            "data": {...},
            "message": str,
        }
    """

    code = str(
        data.get("code", "")
    ).strip().upper()

    description = str(
        data.get("description", "")
    ).strip()

    discount_type = str(
        data.get("discount_type", "")
    ).strip()

    discount_value_raw = str(
        data.get("discount_value", "")
    ).strip()

    minimum_order_raw = str(
        data.get("minimum_order_amount", "0")
    ).strip()

    maximum_discount_raw = str(
        data.get("maximum_discount", "")
    ).strip()

    start_date_raw = str(
        data.get("start_date", "")
    ).strip()

    expiry_date_raw = str(
        data.get("expiry_date", "")
    ).strip()

    usage_limit_raw = str(
        data.get("usage_limit", "")
    ).strip()

    # -----------------------------------------
    # Coupon Code
    # -----------------------------------------

    if not code:
        return {
            "valid": False,
            "data": {},
            "message": "Coupon code is required.",
        }

    if len(code) > 50:
        return {
            "valid": False,
            "data": {},
            "message": (
                "Coupon code cannot exceed 50 characters."
            ),
        }

    # -----------------------------------------
    # Discount Type
    # -----------------------------------------

    if discount_type not in [
        "percentage",
        "fixed",
    ]:
        return {
            "valid": False,
            "data": {},
            "message": "Invalid discount type.",
        }

    # -----------------------------------------
    # Discount Value
    # -----------------------------------------

    try:
        discount_value = Decimal(
            discount_value_raw
        )
    except (
        InvalidOperation,
        ValueError,
        TypeError,
    ):
        return {
            "valid": False,
            "data": {},
            "message": "Invalid discount value.",
        }

    if discount_value <= Decimal("0"):
        return {
            "valid": False,
            "data": {},
            "message": (
                "Discount value must be greater than 0."
            ),
        }

    if (
        discount_type == "percentage"
        and discount_value > Decimal("100")
    ):
        return {
            "valid": False,
            "data": {},
            "message": (
                "Percentage discount cannot exceed 100%."
            ),
        }

    # -----------------------------------------
    # Minimum Order Amount
    # -----------------------------------------

    try:
        minimum_order_amount = Decimal(
            minimum_order_raw or "0"
        )
    except (
        InvalidOperation,
        ValueError,
        TypeError,
    ):
        return {
            "valid": False,
            "data": {},
            "message": (
                "Invalid minimum order amount."
            ),
        }

    if minimum_order_amount < Decimal("0"):
        return {
            "valid": False,
            "data": {},
            "message": (
                "Minimum order amount cannot be negative."
            ),
        }

    # -----------------------------------------
    # Maximum Discount
    # -----------------------------------------

    maximum_discount = None

    if maximum_discount_raw:

        try:
            maximum_discount = Decimal(
                maximum_discount_raw
            )
        except (
            InvalidOperation,
            ValueError,
            TypeError,
        ):
            return {
                "valid": False,
                "data": {},
                "message": (
                    "Invalid maximum discount."
                ),
            }

        if maximum_discount <= Decimal("0"):
            return {
                "valid": False,
                "data": {},
                "message": (
                    "Maximum discount must be greater than 0."
                ),
            }

    # -----------------------------------------
    # Start Date
    # -----------------------------------------

    start_date = parse_datetime(
        start_date_raw
    )

    if not start_date:
        return {
            "valid": False,
            "data": {},
            "message": "Invalid start date.",
        }

    # -----------------------------------------
    # Expiry Date
    # -----------------------------------------

    expiry_date = parse_datetime(
        expiry_date_raw
    )

    if not expiry_date:
        return {
            "valid": False,
            "data": {},
            "message": "Invalid expiry date.",
        }

    # -----------------------------------------
    # Timezone Handling
    # -----------------------------------------

    if timezone.is_naive(start_date):
        start_date = timezone.make_aware(
            start_date
        )

    if timezone.is_naive(expiry_date):
        expiry_date = timezone.make_aware(
            expiry_date
        )

    # -----------------------------------------
    # Date Validation
    # -----------------------------------------

    if expiry_date <= start_date:
        return {
            "valid": False,
            "data": {},
            "message": (
                "Expiry date must be later than start date."
            ),
        }

    # -----------------------------------------
    # Usage Limit
    # -----------------------------------------

    usage_limit = None

    if usage_limit_raw:

        try:
            usage_limit = int(
                usage_limit_raw
            )
        except (
            ValueError,
            TypeError,
        ):
            return {
                "valid": False,
                "data": {},
                "message": "Invalid usage limit.",
            }

        if usage_limit <= 0:
            return {
                "valid": False,
                "data": {},
                "message": (
                    "Usage limit must be greater than 0."
                ),
            }

    # -----------------------------------------
    # Duplicate Coupon Code Check
    # -----------------------------------------

    duplicate_query = Coupon.objects.filter(
        code__iexact=code
    )

    # When updating an existing coupon,
    # exclude itself from duplicate check.
    if coupon is not None:
        duplicate_query = duplicate_query.exclude(
            id=coupon.id
        )

    if duplicate_query.exists():
        return {
            "valid": False,
            "data": {},
            "message": (
                "A coupon with this code already exists."
            ),
        }

    # -----------------------------------------
    # Cleaned Data
    # -----------------------------------------

    cleaned_data = {
        "code": code,
        "description": description,
        "discount_type": discount_type,
        "discount_value": discount_value,
        "minimum_order_amount": minimum_order_amount,
        "maximum_discount": maximum_discount,
        "start_date": start_date,
        "expiry_date": expiry_date,
        "usage_limit": usage_limit,
    }

    return {
        "valid": True,
        "data": cleaned_data,
        "message": "Coupon data is valid.",
    }