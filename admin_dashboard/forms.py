from django import forms
from .models import Category
from .models import *

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





