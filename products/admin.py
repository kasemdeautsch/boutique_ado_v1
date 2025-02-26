from django.contrib import admin
from .models import Product, Category

# Register your models here.
"""
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'friendly_name')
    search_fields = ['name']
    list_filter = ('name',)
"""

admin.site.register(Product)
admin.site.register(Category)
