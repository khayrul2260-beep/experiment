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