from django.db import models

# Create your models here.
class Fragrance(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField()
    stock =  models.IntegerField()
    img = models.CharField(max_length=2083)
