from django.contrib import admin
import products.models

admin.site.register(products.models.ProductCategory)


@admin.register(products.models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'category')
    fields = ('name', 'description', ('price', 'quantity'), 'category', 'image')
    ordering = ('name',)
    search_fields = ('name', 'price')
