from django.db import models

class Fragrance(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField()
    salePrice = models.FloatField(null=True, blank=True)
    category =  models.CharField(max_length=255)
    img = models.CharField(max_length=2083)
    isOnSale = models.BooleanField(default=False)
