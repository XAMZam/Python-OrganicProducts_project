from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    weight = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    image = models.CharField(max_length=250, null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

class Shampoo(Product):
    pass

class Scrub(Product):
    pass

class FaceCleanser(Product):
    pass

class BodySoap(Product):
    pass

class LiquidSoap(Product):
    pass

class Oil(Product):
    pass
