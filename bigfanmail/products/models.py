from django.db import models

# Create your models here.
class Product(models.Model):
    price =           models.DecimalField(max_digits=6, decimal_places=2)
    product_name =    models.CharField(max_length=50, unique=True)
    description =     models.CharField(max_length=150)

    def __unicode__(self):
        return self.product_name

class CommonName(models.Model):
    common_name =    models.CharField(max_length=30, unique=True)

    def __unicode__(self):
        return self.common_name

class Occupation(models.Model):
    occupation =     models.CharField(max_length=50, unique=True)

    def __unicode__(self):
        return self.occupation

