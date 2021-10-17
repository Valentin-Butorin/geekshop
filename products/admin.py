from django.contrib import admin
import products.models

admin.site.register(products.models.Product)
admin.site.register(products.models.ProductCategory)
