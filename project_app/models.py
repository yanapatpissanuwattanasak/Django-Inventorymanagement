from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Tables(models.Model):
    name = models.TextField()
    desc = models.TextField()

class Personal(models.Model):
    username = models.CharField(max_length=50)
    rank = models.CharField(max_length=50)
    email    = models.EmailField()
    fullname    = models.TextField()
    identification = models.CharField(max_length=30)
    phone = models.TextField()
    shop_name = models.CharField(max_length=50)
    address_id = models.CharField(max_length=50)
    address_t = models.CharField(max_length=50)
    address_a = models.CharField(max_length=50)
    address_city = models.CharField(max_length=50)
    address_post = models.CharField(max_length=50)
    address_desc = models.TextField()

class Manufacturer(models.Model):
    fact_name = models.CharField(max_length=50)
    fact_id = models.CharField(max_length=20)
    fact_t = models.TextField()
    fact_a = models.TextField()
    fact_city = models.TextField()
    fact_post = models.CharField(max_length=20)
    fact_email = models.EmailField()
    fact_phone = models.CharField(max_length=20)
    fact_desc = models.TextField()
    

class Product(models.Model):
    product_code = models.CharField(max_length=20)
    product_name = models.CharField(max_length=50)
    product_type = models.CharField(max_length=50)
    product_size = models.CharField(max_length=10)
    product_send_time = models.IntegerField()
    product_cost = models.IntegerField()
    product_selling = models.IntegerField()
    product_balance = models.IntegerField(default=0)
    product_image = models.FileField()
    product_desc = models.TextField()
    prodect_status = models.CharField(max_length=50)
    product_fact_name = models.CharField(max_length=50)

class History_input(models.Model):
    history_product_code = models.CharField(max_length=20)
    history_balance = models.IntegerField()
    history_total = models.IntegerField()
    history_date = models.DateField()
    history_user = models.CharField(max_length=50)
    
class Product_output(models.Model):
    product_code = models.CharField(max_length=20)
    product_quantity = models.PositiveIntegerField()
    date_output = models.DateField()

class Shelf(models.Model):
    code1_4 = models.CharField(max_length=4)
    code5_6 = models.CharField(max_length=2)
    code7_9 = models.CharField(max_length=3)
    code = models.TextField(max_length=50, blank=True)
    value = models.IntegerField()
    valueremain = models.IntegerField(default=0)

class preorder(models.Model):
    product_code = models.CharField(max_length=20)
    balance = models.IntegerField()
    employee = models.CharField(max_length=50)
    date = models.DateField()

class Basket(models.Model):
    product_code = models.CharField(max_length=20)
    qty = models.IntegerField()
    employee = models.CharField(max_length=50)
    status = models.CharField(max_length=50)

class store_stock(models.Model) :
    store_id = models.CharField(max_length=20)
    product_code = models.CharField(max_length=20)
    qty = models.IntegerField()
    status = models.CharField(max_length=20)

class Store(models.Model):
    store_name = models.CharField(max_length=50)
    store_id = models.CharField(max_length=20)
    store_t = models.TextField()
    store_a = models.TextField()
    store_city = models.TextField()
    store_post = models.CharField(max_length=20)
    store_email = models.EmailField()
    store_phone = models.CharField(max_length=20)
    store_desc = models.TextField()

class Order(models.Model):
    order_id = models.CharField(max_length=50)
    shop_name = models.CharField(max_length=50)
    employee = models.CharField(max_length=50)
    date = models.DateField()
    date_sended = models.DateField(default=None, blank=True)
    status = models.CharField(max_length=50)

class saled(models.Model):
    product_code = models.CharField(max_length=20)
    shop_name = models.CharField(max_length=50)
    employee = models.CharField(max_length=50)
    date = models.DateField()
    qty = models.IntegerField()
    total = models.IntegerField()

class product_shelf(models.Model):
    product_code = models.CharField(max_length=20)
    shelf_id = models.TextField(max_length=50, blank=True)
    qty = models.IntegerField()
    status = models.CharField(max_length=50)
    
class check(models.Model):
    product_code = models.CharField(max_length=20)
    shelf_id = models.TextField(max_length=50, blank=True)
    qty = models.IntegerField()
    employee = models.CharField(max_length=50)
    date = models.DateField()
    time = models.TimeField()
class lost_list(models.Model) :
    product_code = models.CharField(max_length=20)
    shelf_id = models.TextField(max_length=50, blank=True)
    qty = models.IntegerField()

