from django.db import models

from users.models import User

# Create your models here.
class ProductCategory(models.Model):
    name = models.CharField(max_length=128, unique=True, verbose_name='Категория')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название вещи')
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Цена')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Количество')
    image = models.ImageField(upload_to='products_images', verbose_name='Изображение')
    category = models.ForeignKey(to=ProductCategory, on_delete=models.CASCADE, verbose_name='Категория')

    def __str__(self):
        return f'Продукт: {self.name} | Категория: {self.category}'

class BasketQuerySet(models.QuerySet):
    def total_sum(self):
        #baskets = Basket.objects.filter(user=self.user)
        return sum(basket.sum() for basket in self) #self = baskets

    def total_quantity(self):
        #baskets = Basket.objects.filter(user=self.user)
        return sum(basket.quantity for basket in self) #self = baskets

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
