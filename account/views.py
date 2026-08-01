from django.shortcuts import render, redirect
# from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


def register_page(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        conf_password = request.POST.get('conf_password')

        if password == conf_password:

            User.objects.create_user(
                username = username,
                email = email,
                password = password
            )
            return redirect('login_page')


    else:
        print("Password not match.")
    return render(request, 'register.html')

def login_page(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)

            if user.is_staff:
                return redirect("dashboard_page")
            
            else:
                return redirect("home_page")
    
        else:
            print("Invalid password.")


    return render(request, 'login.html')
