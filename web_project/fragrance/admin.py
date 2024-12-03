from django.contrib import admin
from .models import Fragrance, Cart

# Register your models here.

class FragranceAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'price', 'salePrice', 'category', 'img', 'isOnSale')

admin.site.register(Fragrance, FragranceAdmin)

class CartAdmin(admin.ModelAdmin):
    list_display = ('fragrance', 'quantity', 'total')

admin.site.register(Cart, CartAdmin)