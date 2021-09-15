from django.db import models

# Create your models here.


class Shop(models.Model):
    name = models.CharField(max_length=100)
    owner = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Item(models.Model):
    name = models.CharField(max_length=100)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    product_image = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
