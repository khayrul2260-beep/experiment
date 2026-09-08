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


    path("about/", about_management, name="about_management"),

    path("about/update/", update_about_page, name="update_about_page"),

    path("about/value/add/", add_about_value, name="add_about_value"),

    path("about/value/<int:value_id>/delete/", delete_about_value, name="delete_about_value"),

    path("about/quality/add/", add_about_quality, name="add_about_quality"),

    path("about/quality/<int:quality_id>/delete/", delete_about_quality, name="delete_about_quality"),

    path("about/journey/add/", add_about_journey, name="add_about_journey"),

    path("about/journey/<int:journey_id>/delete/", delete_about_journey, name="delete_about_journey"),

    path("about/value/<int:value_id>/update/", update_about_value, name="update_about_value"),

    path("about/quality/<int:quality_id>/update/", update_about_quality, name="update_about_quality"),
    path("about/journey/<int:journey_id>/update/", update_about_journey, name="update_about_journey"),
]