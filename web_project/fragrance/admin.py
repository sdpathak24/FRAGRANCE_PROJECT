from django.contrib import admin
from .models import Fragrance

# Register your models here.

class FragranceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock')

admin.site.register(Fragrance, FragranceAdmin)