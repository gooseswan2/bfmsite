from django.contrib import admin

from bigfanmail.products.models import Product, CommonName, Occupation

admin.site.register(Product)
admin.site.register(CommonName)
admin.site.register(Occupation)
