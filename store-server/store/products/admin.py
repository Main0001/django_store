from django.contrib import admin

# Register your models here.
from products.models import Product, ProductCategory, Basket

#admin.site.register(Product)
admin.site.register(ProductCategory)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'category')

    readonly_fields = ('description',)
    fields = ('name', 'description', ('price', 'quantity'), 'image', 'stripe_product_price_id', 'category')
    search_fields = ('name',)
    ordering = ('name',)


class BasketAdmin(admin.TabularInline):
    model = Basket
    fields = ('product', 'quantity')
    extra = 0 #Убирает дополнительные поля в админке
