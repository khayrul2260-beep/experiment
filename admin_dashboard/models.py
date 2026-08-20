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



