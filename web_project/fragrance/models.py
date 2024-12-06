# from django.db import models

# class Fragrance(models.Model):
#     name = models.CharField(max_length=255)
#     brand = models.CharField(max_length=255)
#     price = models.FloatField()
#     salePrice = models.FloatField(null=True, blank=True)
#     category =  models.CharField(max_length=255)
#     img = models.CharField(max_length=2083)
#     isOnSale = models.BooleanField(default=False)

# class Cart(models.Model):
#     fragrance = models.ForeignKey(Fragrance, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1)

#     def total(self):
#         return (self.fragrance.salePrice or self.fragrance.price) * self.quantity

# models.py
from django.db import models

class Fragrance(models.Model):
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    price = models.FloatField()
    salePrice = models.FloatField(null=True, blank=True)
    category =  models.CharField(max_length=255)
    img = models.CharField(max_length=2083)
    isOnSale = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Cart(models.Model):
    fragrance = models.ForeignKey(Fragrance, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total(self):
        return (self.fragrance.salePrice or self.fragrance.price) * self.quantity

