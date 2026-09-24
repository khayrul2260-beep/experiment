from django.contrib import admin
from .models import *
from django.apps import apps


for model in apps.get_app_config("experiment1").get_models():

    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass