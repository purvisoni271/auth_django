from django.db import models


class Product(models.Model):
    product_name = models.CharField(max_length=250)
    product_price = models.IntegerField()
    product_quantity = models.IntegerField()
    product_image = models.FileField(upload_to='product')
    product_description = models.TextField()
