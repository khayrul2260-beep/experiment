from django.db import models
from django.core.exceptions import ValidationError
from PIL import Image
from django.conf import settings
from admin_dashboard.models import *

def validate_desktop_hero_image(image):
    """
    Desktop hero image must be exactly 1968 x 799 pixels.
    """

    required_width = 1968
    required_height = 799

    if image:
        width = image.width
        height = image.height

        if width != required_width or height != required_height:
            raise ValidationError(
                f"Desktop hero image must be exactly "
                f"{required_width} × {required_height} pixels. "
                f"Uploaded image is {width} × {height} pixels."
            )


def validate_mobile_hero_image(image):
    """
    Mobile hero image must be exactly 900 x 1600 pixels.
    """

    required_width = 900
    required_height = 1600

    if image:
        width = image.width
        height = image.height

        if width != required_width or height != required_height:
            raise ValidationError(
                f"Mobile hero image must be exactly "
                f"{required_width} × {required_height} pixels. "
                f"Uploaded image is {width} × {height} pixels."
            )


class HomePage(models.Model):
    """
    Main homepage configuration.
    Ideally only one HomePage record should exist.
    """

    second_hero_image = models.ImageField(
        upload_to="home/second-hero/",
        blank=True,
        null=True
    )
    
    second_hero_is_active = models.BooleanField(
        default=True
    )


    hero_subtitle = models.CharField(
        max_length=150,
        default="PREMIUM MEN'S FASHION"
    )

    hero_title = models.CharField(
        max_length=200,
        default="STYLE THAT DEFINES YOU."
    )

    hero_button_text = models.CharField(
        max_length=100,
        default="EXPLORE COLLECTION"
    )

    hero_button_link = models.CharField(
        max_length=255,
        default="/shop/"
    )

    hero_is_active = models.BooleanField(
        default=True
    )

    categories_is_active = models.BooleanField(
        default=True
    )

    all_products_is_active = models.BooleanField(
        default=True
    )

    featured_is_active = models.BooleanField(
        default=True
    )

    new_arrivals_is_active = models.BooleanField(
        default=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return "NAFI Homepage Settings"

    class Meta:
        verbose_name = "Home Page"
        verbose_name_plural = "Home Page"


class HomeHeroSlide(models.Model):
    """
    Homepage hero slider images.
    """

    home_page = models.ForeignKey(
        HomePage,
        on_delete=models.CASCADE,
        related_name="hero_slides"
    )

    desktop_image = models.ImageField(
        upload_to="home/hero/desktop/",
        validators=[validate_desktop_hero_image]
    )

    mobile_image = models.ImageField(
        upload_to="home/hero/mobile/",
        blank=True,
        null=True,
        validators=[validate_mobile_hero_image]
    )

    alt_text = models.CharField(
        max_length=255,
        blank=True
    )

    display_order = models.PositiveIntegerField(
        default=0
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"Hero Slide #{self.display_order}"

    class Meta:
        ordering = ["display_order", "-created_at"]
        verbose_name = "Home Hero Slide"
        verbose_name_plural = "Home Hero Slides"




# =========================================================
# CART
# =========================================================

class Cart(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cart"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"Cart - {self.user}"

    @property
    def total_items(self):
        return sum(
            item.quantity
            for item in self.items.all()
        )

    @property
    def subtotal(self):
        return sum(
            item.total_price
            for item in self.items.all()
        )


# =========================================================
# CART ITEM
# =========================================================

class CartItem(models.Model):

    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items"
    )

    product = models.ForeignKey(
        ProductsModel,
        on_delete=models.CASCADE,
        related_name="cart_items"
    )

    size = models.CharField(
        max_length=10,
        choices=ProductSize.SIZE_CHOICES
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "cart",
                    "product",
                    "size"
                ],
                name="unique_cart_product_size"
            )
        ]

    def __str__(self):
        return (
            f"{self.product.name} - "
            f"{self.size} × {self.quantity}"
        )

    @property
    def unit_price(self):
        return (
            self.product.discount_price
            if self.product.discount_price
            else self.product.price
        )

    @property
    def total_price(self):
        return self.unit_price * self.quantity


# =========================================================
# WISHLIST
# =========================================================

class Wishlist(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="wishlist"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"Wishlist - {self.user}"


# =========================================================
# WISHLIST ITEM
# =========================================================

class WishlistItem(models.Model):

    wishlist = models.ForeignKey(
        Wishlist,
        on_delete=models.CASCADE,
        related_name="items"
    )

    product = models.ForeignKey(
        ProductsModel,
        on_delete=models.CASCADE,
        related_name="wishlist_items"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "wishlist",
                    "product"
                ],
                name="unique_wishlist_product"
            )
        ]

    def __str__(self):
        return self.product.name