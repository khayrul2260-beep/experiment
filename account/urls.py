from django.urls import path
from .views import *


urlpatterns = [
    path('', register_page, name='register_page'),
    path('login/', login_page, name='login_page'),
]