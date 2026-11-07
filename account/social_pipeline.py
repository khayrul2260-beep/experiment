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
    strategy, backend, user=None, is_new=False, *args, **kwargs
):
    if user is None:
        return {}

    if backend.name != "google-oauth2":
        return {}

    request = strategy.request

    # Admin verification must not run the customer cart merge.
    if request and request.session.get("nafi_admin_google_verify_user_id"):
        return {}

    if request is not None:
        merge_guest_cart_into_user_cart(request, user)

    return {}

def verify_admin_google_identity(
    backend, uid=None, user=None, *args, **kwargs
):
    from django.core.exceptions import PermissionDenied
    from social_django.models import UserSocialAuth

    request = backend.strategy.request
    target_user_id = request.session.get(
        "nafi_admin_google_verify_user_id"
    )

    # Normal customer Google login: no change.
    if not target_user_id:
        return {}

    if (
        backend.name != "google-oauth2"
        or user is None
        or not user.is_authenticated
        or user.pk != target_user_id
    ):
        request.session.pop("nafi_admin_google_verify_user_id", None)
        raise PermissionDenied("Admin Google verification failed.")

    linked = UserSocialAuth.objects.filter(
        user_id=target_user_id,
        provider="google-oauth2",
        uid=uid,
    ).exists()

    if not linked:
        request.session.pop("nafi_admin_google_verify_user_id", None)
        raise PermissionDenied(
            "This Google account is not linked to your NAFI account."
        )

    return {}


def complete_admin_google_verification(
    strategy, backend, uid=None, user=None, *args, **kwargs
):
    from django.core.exceptions import PermissionDenied
    from django.urls import reverse
    from social_django.models import UserSocialAuth

    request = strategy.request
    target_user_id = request.session.get(
        "nafi_admin_google_verify_user_id"
    )

    if not target_user_id:
        return {}

    if (
        backend.name != "google-oauth2"
        or user is None
        or not user.is_authenticated
        or user.pk != target_user_id
    ):
        request.session.pop("nafi_admin_google_verify_user_id", None)
        raise PermissionDenied("Admin verification failed.")

    linked = UserSocialAuth.objects.filter(
        user_id=target_user_id,
        provider="google-oauth2",
        uid=uid,
    ).exists()

    if not linked:
        request.session.pop("nafi_admin_google_verify_user_id", None)
        raise PermissionDenied("Google identity verification failed.")

    from admin_dashboard.permissions import get_admin_role

    if get_admin_role(user) is None or not user.is_active:
        request.session.pop("nafi_admin_google_verify_user_id", None)
        raise PermissionDenied("Admin access is not allowed.")

    request.session["admin_verified"] = True
    request.session["admin_verified_user_id"] = user.pk
    request.session["admin_verified_auth_hash"] = (
        user.get_session_auth_hash()
    )

    request.session["next"] = reverse("dashboard_page")
    request.session.pop("nafi_admin_google_verify_user_id", None)

    return {}