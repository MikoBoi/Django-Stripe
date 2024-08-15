from django.db import models

# Create your models here.

class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    price = models.IntegerField()

    def __str__(self):
        return self.name

    def get_decimal_price(self):
        return "{0:.2f}".format(self.price / 100)