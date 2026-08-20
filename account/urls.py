from django.urls import path
from .views import *


urlpatterns = [
    path('', customer_register, name='customer_register'),
    path('login/', customer_login, name='customer_login'),
    path('logout/', customer_logout, name="customer_logout"),    
    path('profile/', customer_profile, name="customer_profile"),    
    path('edit_profile/', customer_edit_profile, name="customer_edit_profile"),    
    path('change_password/', customer_change_password, name="customer_change_password"),    
]