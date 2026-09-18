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

            # Full name
            user.first_name = form.cleaned_data["full_name"]

            # Secure password hashing
            user.set_password(
                form.cleaned_data["password"]
            )

            user.save()

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

            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(
                request,
                username=username,
                password=password
            )

            if user is not None:
            
                login(request, user)
            
                merge_guest_cart_into_user_cart(
                    request,
                    user
                )
            
                return redirect("customer_profile")

            messages.error(
                request,
                "Invalid phone number or password."
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

    return render(
        request,
        "account/customer_profile.html"
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