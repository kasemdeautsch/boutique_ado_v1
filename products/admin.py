from django.contrib import admin
from .models import Product, Category

# Register your models here.

#@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name'
    )
    search_fields = ['name']
    list_filter = ('name',)

#@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'sku',
        'name',
        'category',
        'price',
        'rating',
        'image',
        )
    #fields=('category', 'price',('name'))
    search_fields = ['name']
    list_filter = ('name',)
    ordering = ('sku',)

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
