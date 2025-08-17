from django.contrib import admin
from .models import Brand, Category, Product
from django.utils.text import slugify


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "brand", "part_number", "price", "stock")
    search_fields = ("name", "part_number")
    list_filter = ("brand", "category")
    prepopulated_fields = {'slug': ('name',)}  # Автозаполнение slug из name

    def get_readonly_fields(self, request, obj=None):
        if obj:  # При редактировании существующего объекта
            return ('slug',) + self.readonly_fields
        return self.readonly_fields  # При создании разрешаем редактирование

    def save_model(self, request, obj, form, change):
        """Гарантируем заполнение slug даже при ручном создании"""
        if not obj.slug:
            obj.slug = slugify(obj.name)
        super().save_model(request, obj, form, change)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('slug',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
