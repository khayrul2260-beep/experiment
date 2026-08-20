from django.urls import path
from .views import *

urlpatterns = [
    path("", dashboard_page, name="dashboard_page"),
    path('products/', products_page, name='products_page'),
    path('categories/', categories_page, name='categories_page'),
    path('orders/', orders_page, name='orders_page'),
    path('customers/', customers_page, name='customers_page'),
    path('inventory/', inventory_page, name='inventory_page'),
    path('coupons/', coupons_page, name='coupons_page'),
    path('reviews/', reviews_page, name='reviews_page'),
    path('reports/', reports_page, name='reports_page'),
    path('settings/', settings_page, name='settings_page'),
    path('admin_users/', admin_users_page, name='admin_users_page'),
    path('logout/', logout_page, name='logout_page'),
    path('hidden_sidebar/', hidden_sidebar_page, name='hidden_sidebar_page'),
    path("product/add/", add_product_page, name="add_product_page"),
    path("product/edit/<int:id>/", edit_product_page, name="edit_product_page"),
    path("delete/<int:id>/", delete_product_page, name="delete_product_page"),
    path("categories/add/", add_category, name='add_category'),
    path("categories/delete/<int:id>/", delete_category, name="delete_category"),
    path("category/edit/<int:id>/", edit_category, name="edit_category"),
]