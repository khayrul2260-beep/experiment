from django.db import models
import random
import string
from django.apps import apps
from datetime import datetime
from django.utils.text import slugify


# Create your models here.

def generate_product_code():

    ProductsModel = apps.get_model("admin_dashboard", "ProductsModel")
    year = str(datetime.now().year)[-2:]

    while True:

        random_code = ''.join(
            random.choices(
                string.ascii_uppercase + string.digits,
                k=7
            )
        )

        code = f"NAFI-KK-{year}-{random_code}"

        if not ProductsModel.objects.filter(product_code=code).exists():
            return code


class Category(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True
    )

    slug = models.SlugField(
        max_length=120,
        unique=True,
        blank=True
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    image = models.ImageField(
        upload_to='categories/',
        blank=True,
        null=True
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


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)


    def __str__(self):
        return f'{self.name}'




class ProductsModel(models.Model):


    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products'
    )    
    

    STATUS_TYPE = [
        ('Stock', 'Stock'),
        ('Out of stock', 'Out of stock')
    ]


    name = models.CharField(max_length=200)

    product_code = models.CharField(
        max_length=30,
        unique=True,
        editable=False,
        blank=True
    )
    
    slug = models.SlugField(unique=True, blank=True)

    description = models.TextField()

    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )


    stock = models.PositiveIntegerField(default=0)

    image = models.ImageField(upload_to="products/")

    is_available = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        choices=STATUS_TYPE,
        max_length=30,
        default="Stock"
    )



    def save(self, *args, **kwargs):

        if not self.product_code:
            self.product_code = generate_product_code()

        if not self.slug:
            self.slug = slugify(
                f"{self.name}-{self.product_code}"
            )

        # stock status
        if self.stock > 0:
            self.status = "Stock"
        else:
            self.status = "Out of stock"


        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name} - {self.price}'


class ProductImage(models.Model):

    IMAGE_TYPE_CHOICES = [
        ("secondary", "Secondary"),
        ("gallery", "Gallery"),
    ]

    product = models.ForeignKey(
        ProductsModel,
        on_delete=models.CASCADE,
        related_name="images"
    )

    image = models.ImageField(
        upload_to="products/gallery/"
    )

    image_type = models.CharField(
        max_length=20,
        choices=IMAGE_TYPE_CHOICES
    )

    sort_order = models.PositiveIntegerField(
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["sort_order", "created_at"]

        constraints = [
            models.UniqueConstraint(
                fields=["product", "image_type"],
                condition=models.Q(
                    image_type="secondary"
                ),
                name="unique_secondary_image_per_product"
            )
        ]

    def __str__(self):
        return f"{self.product.name} - {self.image_type}"

        

class ProductSize(models.Model):

    SIZE_CHOICES = [
        ('M', 'M'),
        ('L', 'L'),
        ('XL', 'XL'),
        ('XXL', 'XXL'),
    ]

    product = models.ForeignKey(
        ProductsModel,
        on_delete=models.CASCADE,
        related_name='sizes'
    )

    size = models.CharField(
        max_length=10,
        choices=SIZE_CHOICES
    )

    stock = models.PositiveIntegerField(
        default=0
    )

    is_available = models.BooleanField(
        default=True
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
                fields=['product', 'size'],
                name='unique_product_size'
            )
        ]
        ordering = ['size']

    def __str__(self):
        return f'{self.product.name} - {self.size}'


# =========================================================
# NAFI ABOUT PAGE
# =========================================================

class AboutPage(models.Model):
    """
    Main editable content for the NAFI public About / Brand Profile page.
    Keep only ONE active AboutPage record.
    """

    # -----------------------------------------------------
    # HERO
    # -----------------------------------------------------
    hero_eyebrow = models.CharField(
        max_length=80,
        default="NAFI"
    )

    hero_title = models.CharField(
        max_length=160,
        default="DEFINED BY SIMPLICITY."
    )

    hero_description = models.TextField(
        blank=True
    )

    hero_image = models.ImageField(
        upload_to="about/",
        blank=True,
        null=True
    )

    # -----------------------------------------------------
    # WHO WE ARE
    # -----------------------------------------------------
    who_title = models.CharField(
        max_length=160,
        default="WHO IS NAFI?"
    )

    who_content = models.TextField(
        blank=True
    )

    who_image = models.ImageField(
        upload_to="about/",
        blank=True,
        null=True
    )

    # -----------------------------------------------------
    # BRAND ORIGIN
    # -----------------------------------------------------
    origin_title = models.CharField(
        max_length=160,
        default="WHERE IT BEGAN"
    )

    origin_content = models.TextField(
        blank=True
    )

    # -----------------------------------------------------
    # VISION
    # -----------------------------------------------------
    vision_title = models.CharField(
        max_length=160,
        default="OUR VISION"
    )

    vision_statement = models.CharField(
        max_length=300,
        blank=True
    )

    vision_content = models.TextField(
        blank=True
    )

    # -----------------------------------------------------
    # MADE FOR THE MODERN MAN
    # -----------------------------------------------------
    modern_title = models.CharField(
        max_length=160,
        default="MADE FOR THE MODERN MAN"
    )

    modern_content = models.TextField(
        blank=True
    )

    # -----------------------------------------------------
    # NAFI AESTHETIC
    # -----------------------------------------------------
    aesthetic_title = models.CharField(
        max_length=160,
        default="THE NAFI AESTHETIC"
    )

    aesthetic_content = models.TextField(
        blank=True
    )

    aesthetic_image = models.ImageField(
        upload_to="about/",
        blank=True,
        null=True
    )

    # -----------------------------------------------------
    # QUALITY
    # -----------------------------------------------------
    quality_title = models.CharField(
        max_length=160,
        default="QUALITY IS NOT AN OPTION."
    )

    quality_intro = models.TextField(
        blank=True
    )

    # -----------------------------------------------------
    # TRANSPARENCY
    # -----------------------------------------------------
    transparency_title = models.CharField(
        max_length=160,
        default="OUR COMMITMENT TO TRANSPARENCY"
    )

    transparency_content = models.TextField(
        blank=True
    )

    # -----------------------------------------------------
    # WHY NAFI
    # -----------------------------------------------------
    why_title = models.CharField(
        max_length=160,
        default="WHY NAFI?"
    )

    why_content = models.TextField(
        blank=True
    )

    # -----------------------------------------------------
    # NAFI AT A GLANCE
    # -----------------------------------------------------
    profile_title = models.CharField(
        max_length=160,
        default="NAFI AT A GLANCE"
    )

    profile_category = models.CharField(
        max_length=120,
        default="Men's Fashion"
    )

    profile_focus = models.CharField(
        max_length=120,
        default="Modern Menswear"
    )

    profile_style = models.CharField(
        max_length=120,
        default="Minimal & Refined"
    )

    profile_values = models.CharField(
        max_length=255,
        default="Quality • Design • Comfort • Confidence"
    )

    profile_products = models.CharField(
        max_length=255,
        default="T-Shirts • Shirts • Punjabi"
    )

    # -----------------------------------------------------
    # FINAL BRAND STATEMENT
    # -----------------------------------------------------
    final_title = models.CharField(
        max_length=160,
        default="MINIMAL. MASCULINE. TIMELESS."
    )

    final_content = models.TextField(
        blank=True
    )

    final_statement = models.CharField(
        max_length=160,
        default="WEAR YOUR CONFIDENCE."
    )

    cta_text = models.CharField(
        max_length=80,
        default="EXPLORE COLLECTION"
    )

    final_image = models.ImageField(
        upload_to="about/",
        blank=True,
        null=True
    )

    # -----------------------------------------------------
    # STATUS
    # -----------------------------------------------------
    is_published = models.BooleanField(
        default=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = "About Page"
        verbose_name_plural = "About Page"

    def __str__(self):
        return "NAFI About Page"


# =========================================================
# NAFI ABOUT — BRAND VALUES
# =========================================================

class AboutValue(models.Model):

    about_page = models.ForeignKey(
        AboutPage,
        on_delete=models.CASCADE,
        related_name="values"
    )

    title = models.CharField(
        max_length=80
    )

    description = models.TextField()

    icon = models.CharField(
        max_length=80,
        blank=True,
        help_text="Example: bi bi-gem"
    )

    display_order = models.PositiveIntegerField(
        default=0
    )

    is_active = models.BooleanField(
        default=True
    )

    class Meta:
        ordering = [
            "display_order",
            "id"
        ]

    def __str__(self):
        return self.title


# =========================================================
# NAFI ABOUT — QUALITY COMMITMENTS
# =========================================================

class AboutQuality(models.Model):

    about_page = models.ForeignKey(
        AboutPage,
        on_delete=models.CASCADE,
        related_name="quality_items"
    )

    title = models.CharField(
        max_length=100
    )

    description = models.TextField()

    icon = models.CharField(
        max_length=80,
        blank=True,
        help_text="Example: bi bi-check2-circle"
    )

    display_order = models.PositiveIntegerField(
        default=0
    )

    is_active = models.BooleanField(
        default=True
    )

    class Meta:
        ordering = [
            "display_order",
            "id"
        ]

        verbose_name = "About Quality Commitment"
        verbose_name_plural = "About Quality Commitments"

    def __str__(self):
        return self.title


# =========================================================
# NAFI ABOUT — BRAND JOURNEY
# =========================================================

class AboutJourney(models.Model):

    about_page = models.ForeignKey(
        AboutPage,
        on_delete=models.CASCADE,
        related_name="journey_items"
    )

    year = models.CharField(
        max_length=20
    )

    title = models.CharField(
        max_length=160
    )

    description = models.TextField(
        blank=True
    )

    image = models.ImageField(
        upload_to="about/journey/",
        blank=True,
        null=True
    )

    display_order = models.PositiveIntegerField(
        default=0
    )

    is_active = models.BooleanField(
        default=True
    )

    class Meta:
        ordering = [
            "display_order",
            "year",
            "id"
        ]

    def __str__(self):
        return f"{self.year} — {self.title}"