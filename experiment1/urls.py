from django.urls import path
# from django.contrib.auth.models import 
from .views import *

urlpatterns = [
    path('', home_page, name="home_page"),
    path('product/<slug:slug>/', product_detail_page, name='product_detail_page'),

]