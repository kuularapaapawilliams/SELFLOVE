from distutils.command.upload import upload
from email.mime import image
from enum import auto
from random import choices
from tkinter import CASCADE
from turtle import title
from unicodedata import category
from django.db import models
from django.contrib.auth.models import User

class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=60)
    image = models.ImageField(upload_to="admins")
    tel = models.CharField(max_length=18)
    def __str__(self):
        return self.user.username


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    address = models.CharField(max_length=250, null=True, blank=True)
    joined_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name

class Category(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title

class Product(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(unique=True)
    category= models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="products")
    marked_price = models.PositiveBigIntegerField()
    selling_price = models.PositiveBigIntegerField()
    description = models.TextField()
    warranty = models.CharField(max_length=350, null=True, blank=True)
    return_policy = models.CharField(max_length=350, null=True, blank=True)
    view_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="products/images/")

    def __str__(self):
        return self.product.title

class Cart(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, blank=True)
    total = models.PositiveBigIntegerField(default=0)    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return " Cart: " + str(self.id)


class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rate = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    subtotal = models.PositiveBigIntegerField()


    def __str__(self):
       return " Cart: " + str(self.cart.id) + " CartProduct: " + str(self.id)

ORDER_STATUS = (
    ("Order Received", "Order Received"),
    ("Order Processing", "Order Processing"),
    ("On the way", "On the way"),
    ("Order Completed", "Order Completed"),
    ("Order Canceled", "Order Canceled"),
)       

class Order(models.Model):
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    ordered_by = models.CharField(max_length=200)
    shipping_address = models.CharField(max_length=200)
    tel = models.CharField(max_length=15)
    email = models.EmailField(null=True, blank=True)
    subtotal = models.PositiveBigIntegerField()
    discount = models.PositiveBigIntegerField()
    total = models.PositiveBigIntegerField()
    order_status = models.CharField(max_length=60, choices=ORDER_STATUS)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return " Order: " + str(self.id)



