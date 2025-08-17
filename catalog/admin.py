# catalog/admin.py
from django.contrib import admin
from .models import Brand, Category, Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "brand", "part_number", "price", "stock")
    search_fields = ("name", "part_number")
    list_filter = ("brand", "category")
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('slug',)

admin.site.register(Brand)
admin.site.register(Category)