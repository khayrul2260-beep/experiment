from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required


@staff_member_required(login_url="login_page")
def dashboard_page(request):
    return render(request, "admin_dashboard/dashboard.html")

def products_page(request):

    return render(request, 'admin_dashboard/products.html')

def customers_page(request):

    return render(request, 'admin_dashboard/customers.html')

def admin_users_page(request):

    return render(request, 'admin_dashboard/admin_users.html')
