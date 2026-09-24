from django.urls import path
from .views import *

urlpatterns = [
    path('', home_page, name="home_page"),
    path("about/", about_page, name="about"),
    path('product/<slug:slug>/', product_detail_page, name='product_detail_page'),
    path('category/<slug:slug>/', category_products_page, name='category_products'),
    path("contact/", contact_page, name="contact_page"),

    path("cart/", cart_page, name="cart_page"),
    path("cart/add/<int:product_id>/", add_to_cart, name="add_to_cart"),
    path("cart/guest/update/<str:item_key>/", guest_update_cart, name="guest_update_cart"),
    path("cart/guest/update-size/<str:item_key>/", guest_update_cart_size, name="guest_update_cart_size"),
    path("cart/guest/add-another-size/<str:item_key>/", guest_add_another_size, name="guest_add_another_size"),
    path("cart/guest/remove/<str:item_key>/", guest_remove_from_cart, name="guest_remove_from_cart"),
    path("cart/update/<int:item_id>/", update_cart, name="update_cart"),
    path("cart/update-size/<int:item_id>/", update_cart_size, name="update_cart_size" ),
    path("cart/add-another-size/<int:item_id>/", add_another_size, name="add_another_size"),
    path("cart/remove/<int:item_id>/", remove_from_cart, name="remove_from_cart"),
    path("cart/clear/", clear_cart, name="clear_cart"),

    path("checkout/", checkout_page, name="checkout_page"),
    path("order-confirmation/<str:order_number>/", order_confirmation_page, name="order_confirmation"),
    path("my-orders/", my_orders_page, name="my_orders"),
    path("order-details/<str:order_number>/", order_details_page, name="order_details"),
    
    path("wishlist/", wishlist_page, name="wishlist_page"),
    path("wishlist/toggle/<int:product_id>/", add_to_wishlist, name="add_to_wishlist"),
    path("new-arrivals/", new_arrivals_page, name="new_arrivals_page"),
    path("shop/", all_products_page, name="all_products_page"),
]