# catalog/models.py
from django.db import models

class Brand(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to="brands/", blank=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200)
    part_number = models.CharField(max_length=50)  # Уникальный артикул
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    description = models.TextField()
    image = models.ImageField(upload_to="products/")
    created_at = models.DateTimeField(auto_now_add=True)
    specs = models.JSONField(default=dict)  # Характеристики (например, {"weight": "1kg", "color": "red"})

    def __str__(self):
        return f"{self.brand.name} {self.name}" if self.brand else self.name