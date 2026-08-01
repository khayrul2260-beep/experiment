from django.urls import path
# from django.contrib.auth.models import 
from .views import *

urlpatterns = [
    path('', home_page, name="home_page")
]