from django import forms
from .models import Category
from .models import *
from .validators import validate_product_image

class ProductForm(forms.ModelForm):

    class Meta:
        model = ProductsModel
        fields = "__all__"






class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category

        fields = [
            'name',
            'description',
            'image',
            'is_active',
        ]

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter category name',
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter category description',
                'rows': 4,
            }),


            'image': forms.FileInput(
                attrs={
                    "accept": "image/*",
                }
            ),

            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }


    def clean_image(self):
        image = self.files.get(self.add_prefix("image"))

        if image:
            validate_product_image(image)

        return self.cleaned_data.get("image")



