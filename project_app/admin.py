from django.contrib import admin
from .models import Tables,Product,Manufacturer
from django.contrib.auth.models import User
# Register your models here.
admin.site.register(Tables)
admin.site.register(Product)