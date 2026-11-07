from django.shortcuts import render, redirect
# from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import *
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from experiment1.models import Cart, CartItem
from admin_dashboard.models import *
import uuid
from django.db import IntegrityError, transaction


def merge_guest_cart_into_user_cart(request, user):

    guest_cart = request.session.get(
        "guest_cart",
        {}
    )


    if not guest_cart:

        return


    cart, created = Cart.objects.get_or_create(
        user=user
    )


    for data in guest_cart.values():

        product = ProductsModel.objects.filter(
            id=data.get("product_id"),
            is_available=True
        ).first()


        if not product:

            continue


        product_size = ProductSize.objects.filter(
            id=data.get("size_id"),
            product=product,
            is_available=True,
            stock__gt=0
        ).first()


        if not product_size:

            continue


        quantity = int(
            data.get(
                "quantity",
                1
            )
        )


        if quantity <= 0:

            continue


        if quantity > product_size.stock:

            quantity = product_size.stock


        cart_item, created = CartItem.objects.get_or_create(

            cart=cart,

            product=product,

            size=product_size.size,

            defaults={
                "quantity": quantity
            }

        )


        if not created:

            new_quantity = (
                cart_item.quantity +
                quantity
            )


            if new_quantity > product_size.stock:

                new_quantity = product_size.stock


            cart_item.quantity = (
                new_quantity
            )

            cart_item.save()


    request.session.pop(
        "guest_cart",
        None
    )

    request.session.modified = True



User = get_user_model()

def customer_register(request):

    if request.method == "POST":

        form = CustomerRegistrationForm(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            full_name = form.cleaned_data["full_name"].strip()
            name_parts = full_name.split(maxsplit=1)

            user.first_name = name_parts[0]
            user.last_name = (
                name_parts[1] if len(name_parts) > 1 else ""
            )

            # Generate a unique internal username.
            # Phone number is no longer used as username.
            user.username = f"nafi_{uuid.uuid4().hex}"

            user.email = form.cleaned_data["email"]
            user.phone = form.cleaned_data.get("phone", "")

            # Secure password hashing
            user.set_password(
                form.cleaned_data["password"]
            )

            try:
                with transaction.atomic():
                    user.save()

            except IntegrityError:
                form.add_error(
                    "email",
                    "An account with this email already exists."
                )

            else:
                messages.success(
                    request,
                    "Account created successfully."
                )

                return redirect("customer_login")

    else:
        form = CustomerRegistrationForm()

    return render(
        request,
        "account/register.html",
        {
            "form": form
        }
    )


def customer_login(request):

    if request.method == "POST":

        form = CustomerLoginForm(request.POST)

        if form.is_valid():

            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            # Find the customer using their email address.
            user_account = User.objects.filter(
                email__iexact=email
            ).first()

            user = None

            if user_account is not None:

                # Authenticate through Django's existing backend.
                user = authenticate(
                    request,
                    username=user_account.username,
                    password=password
                )

            if user is not None and user.is_active:

                login(request, user)

                # Preserve existing guest cart merge behavior.
                merge_guest_cart_into_user_cart(
                    request,
                    user
                )

                return redirect("customer_profile")

            messages.error(
                request,
                "Invalid email address or password."
            )

    else:

        form = CustomerLoginForm()

    return render(
        request,
        "account/login.html",
        {
            "form": form
        }
    )


@login_required(login_url="login")
def customer_logout(request):

    logout(request)

    return redirect("home_page")


@login_required(login_url="login")
def customer_profile(request):

    from admin_dashboard.permissions import get_admin_role

    is_admin = get_admin_role(request.user) is not None

    return render(
        request,
        "account/customer_profile.html",
        {
            "is_admin": is_admin,
        }
    )

@login_required(login_url="login")
def admin_password_verify(request):

    from django.contrib.auth.hashers import check_password
    from admin_dashboard.permissions import get_admin_role
    from django.http import Http404
    # Verify current admin authorization
    if get_admin_role(request.user) is None:
        raise Http404("Page not found.")

    # Already verified Admin: skip password verification
    if (
        request.session.get("admin_verified") is True
        and request.session.get("admin_verified_user_id") == request.user.pk
        and request.session.get("admin_verified_auth_hash")
        == request.user.get_session_auth_hash()
    ):
        return redirect("dashboard_page")

    if request.method == "POST":

        password = request.POST.get("password", "")

        if check_password(password, request.user.password):
        
            request.session["admin_verified"] = True

            request.session["admin_verified_user_id"] = (
                request.user.pk
            )

            request.session["admin_verified_auth_hash"] = (
                request.user.get_session_auth_hash()
            )

            messages.success(
                request,
                "Admin access verified successfully."
            )

            return redirect("dashboard_page")

        messages.error(
            request,
            "Incorrect password. Please try again."
        )

    return render(
        request,
        "account/admin_password_verify.html"
    )

@login_required(login_url="login")
def admin_google_verify_begin(request):
    from django.contrib import messages
    from django.shortcuts import redirect
    from django.urls import reverse
    from social_django.models import UserSocialAuth
    from admin_dashboard.permissions import get_admin_role

    if not request.user.is_active or get_admin_role(request.user) is None:
        from django.http import Http404
        raise Http404("Page not found.")

    # Only an already-linked Google identity is accepted.
    linked_google = UserSocialAuth.objects.filter(
        user=request.user,
        provider="google-oauth2",
    ).exists()

    if not linked_google:
        messages.error(
            request,
            "No Google account is linked to your NAFI account. "
            "Please use your account password."
        )
        return redirect("admin_password_verify")

    request.session["nafi_admin_google_verify_user_id"] = request.user.pk
    request.session["next"] = reverse("dashboard_page")

    return render(
        request,
        "account/admin_google_verify_start.html",
        {
            "social_begin_url": reverse(
                "social:begin",
                kwargs={"backend": "google-oauth2"}
            )
        }
    )

@login_required
def customer_edit_profile(request):

    if request.method == "POST":

        form = CustomerProfileForm(
            request.POST,
            request.FILES,
            instance=request.user
        )

        if form.is_valid():

            form.save()

            return redirect("customer_profile")

    else:

        form = CustomerProfileForm(
            instance=request.user
        )

    return render(
        request,
        "account/customer_edit_profile.html",
        {
            "form": form
        }
    )



      
@login_required(login_url="login")
def customer_change_password(request):

    if request.method == "POST":

        form = CustomerPasswordChangeForm(
            request.user,
            request.POST
        )

        if form.is_valid():
        
            user = form.save()

            update_session_auth_hash(
                request,
                user
            )

            # Invalidate previous Admin verification
            request.session.pop("admin_verified", None)
            request.session.pop("admin_verified_user_id", None)
            request.session.pop("admin_verified_auth_hash", None)

            messages.success(
                request,
                "Password changed successfully."
            )

            return redirect("customer_profile")

    else:

        form = CustomerPasswordChangeForm(
            request.user
        )

    return render(
        request,
        "account/change_password.html",
        {
            "form": form
        }
    )