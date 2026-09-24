from django.urls import path
from .views import *
from .contact_views import *
from .customer_views import *


urlpatterns = [
    path("", dashboard_page, name="dashboard_page"),
    path('products/', products_page, name='products_page'),
    path('categories/', categories_page, name='categories_page'),

    path('orders/', orders_page, name='orders_page'),
    path("orders/<str:order_number>/", order_details_page, name="admin_order_details"),
    path("orders/<str:order_number>/update-status/", update_order_status, name="update_order_status"),

    path('customers/', customers_page, name='customers_page'),
    path('inventory/', inventory_page, name='inventory_page'),
    path('coupons/', coupons_page, name='coupons_page'),
    path('reviews/', reviews_page, name='reviews_page'),
    path('reports/', reports_page, name='reports_page'),


    path('settings/', settings_page, name='settings_page'),
    path('settings/home/', home_management, name='home_management'),
    path('settings/home/update/', update_home_page, name='update_home_page'),
    path("settings/home/visibility/update/", update_home_visibility, name="update_home_visibility"),
    path("settings/home/second-hero/update/", update_second_hero, name="update_second_hero"),
    path('settings/home/slide/add/', add_home_slide, name='add_home_slide'),
    path('settings/home/slide/<int:slide_id>/update/', update_home_slide, name='update_home_slide'),
    path('settings/home/slide/<int:slide_id>/delete/', delete_home_slide, name='delete_home_slide'),
    path("settings/about/", about_management, name="about_management"),
    path("settings/about/update/", update_about_page, name="update_about_page"),
    path("settings/about/value/add/", add_about_value, name="add_about_value"),
    path("settings/about/value/<int:value_id>/delete/", delete_about_value, name="delete_about_value"),
    path("settings/about/quality/add/", add_about_quality, name="add_about_quality"),
    path("settings/about/quality/<int:quality_id>/delete/", delete_about_quality, name="delete_about_quality"),
    path("settings/about/journey/add/", add_about_journey, name="add_about_journey"),
    path("settings/about/journey/<int:journey_id>/delete/", delete_about_journey, name="delete_about_journey"),
    path("settings/about/value/<int:value_id>/update/", update_about_value, name="update_about_value"),
    path("settings/about/quality/<int:quality_id>/update/", update_about_quality, name="update_about_quality"),
    path("settings/about/journey/<int:journey_id>/update/", update_about_journey, name="update_about_journey"),


    path("settings/contact/", contact_management, name="contact_management"),
    path("settings/contact/service/add/", add_contact_service, name="add_contact_service"),
    path("settings/contact/service/<int:service_id>/update/", update_contact_service, name="update_contact_service"),
    path("settings/contact/service/<int:service_id>/delete/", delete_contact_service, name="delete_contact_service"),
    path("settings/contact/faq/add/", add_contact_faq, name="add_contact_faq"),
    path("settings/contact/faq/<int:faq_id>/update/", update_contact_faq, name="update_contact_faq"),
    path("settings/contact/faq/<int:faq_id>/delete/", delete_contact_faq, name="delete_contact_faq"),
    path("settings/contact/social/add/",add_contact_social_link,name="add_contact_social_link"),
    path("settings/contact/social/<int:social_id>/update/",update_contact_social_link,name="update_contact_social_link"),
    path("settings/contact/social/<int:social_id>/delete/",delete_contact_social_link,name="delete_contact_social_link"),


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