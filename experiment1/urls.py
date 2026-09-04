from django.urls import path
from .views import *

urlpatterns = [
    path('', home_page, name="home_page"),
    path('product/<slug:slug>/', product_detail_page, name='product_detail_page'),
    path('category/<slug:slug>/', category_products_page, name='category_products'),
]