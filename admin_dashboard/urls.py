from django.urls import path
from .views import *

urlpatterns = [
    path("", dashboard_page, name="dashboard_page"),
    path('products/', products_page, name='products_page'),
    path('customers/', customers_page, name='customers_page'),
    path('admin_users/', admin_users_page, name='admin_users_page'),
]