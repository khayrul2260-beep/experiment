from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied

from .views import merge_guest_cart_into_user_cart


def associate_verified_google_email(
    backend,
    details,
    response,
    user=None,
    *args,
    **kwargs
):
    # Only handle Google OAuth.
    if backend.name != "google-oauth2":
        return {}

    # Already associated with an existing Google account.
    if user is not None:
        return {}

    email = (details.get("email") or "").strip().lower()

    # Never associate an account using an unverified email.
    if not email or response.get("email_verified") is not True:
        raise PermissionDenied(
            "Google email verification is required."
        )

    User = get_user_model()

    existing_user = User.objects.filter(
        email__iexact=email
    ).first()

    if existing_user is None:
        return {}

    if not existing_user.is_active:
        raise PermissionDenied("This account is inactive.")

    return {
        "user": existing_user,
        "is_new": False,
    }


def merge_google_guest_cart(
    strategy,
    backend,
    user=None,
    is_new=False,
    *args,
    **kwargs
):
    if user is None:
        return {}

    if backend.name != "google-oauth2":
        return {}

    request = strategy.request

    if request is not None:
        merge_guest_cart_into_user_cart(
            request,
            user
        )

    return {}