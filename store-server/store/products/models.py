from typing import Iterable, Optional
from django.db import models
from django.conf import settings

import stripe

from users.models import User

stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your models here.
class ProductCategory(models.Model):
    name = models.CharField(max_length=128, unique=True, verbose_name='Категория')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название вещи')
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Цена')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Количество')
    image = models.ImageField(upload_to='products_images', verbose_name='Изображение')
    stripe_product_price_id = models.CharField(max_length=128, null=True, blank=True)
    category = models.ForeignKey(to=ProductCategory, on_delete=models.CASCADE, verbose_name='Категория')

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return f'Продукт: {self.name} | Категория: {self.category}'
    
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.stripe_product_price_id:
            stripe_product_price = self.create_stripe_product_price()
            self.stripe_product_price_id = stripe_product_price['id']
        super(Product, self).save(force_insert, force_update, using, update_fields)
    
    def create_stripe_product_price(self):
        stripe_product = stripe.Product.create(name=self.name)
        stripe_product_price = stripe.Price.create(
            product=stripe_product['id'], unit_amount=round(self.price * 100), currency='rub'
        )
        return stripe_product_price

class BasketQuerySet(models.QuerySet):
    def total_sum(self):
        #baskets = Basket.objects.filter(user=self.user)
        return sum(basket.sum() for basket in self) #self = baskets

    def total_quantity(self):
        #baskets = Basket.objects.filter(user=self.user)
        return sum(basket.quantity for basket in self) #self = baskets
    
    def stripe_products(self):
        line_items = []

        for basket in self:
           item = {
                  'price': basket.product.stripe_product_price_id,
                  'quantity': basket.quantity
           }
           line_items.append(item)
        return line_items

class Basket(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    
    objects = BasketQuerySet.as_manager()

    def __str__(self):
        return f'Корзина для {self.user.username} | Продукт {self.product.name}'
    
    def sum(self):
        return self.product.price * self.quantity
    
    def de_json(self):
        basket_item = {
            'product_name': self.product.name,
            'quantity': self.quantity,
            'price': float(self.product.price),
            'sum': float(self.sum())
        }
        return basket_item
