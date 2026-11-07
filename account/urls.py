from django.urls import path
from .views import *


urlpatterns = [
    path('', customer_register, name='customer_register'),
    path('login/', customer_login, name='customer_login'),
    path('logout/', customer_logout, name="customer_logout"),    
    path('profile/', customer_profile, name="customer_profile"), 
    path('admin-password-verify/', admin_password_verify, name='admin_password_verify'), 
    path("admin-google-verify/", admin_google_verify_begin, name="admin_google_verify_begin"),
    path('edit_profile/', customer_edit_profile, name="customer_edit_profile"),    
    path('change_password/', customer_change_password, name="customer_change_password"),    
]