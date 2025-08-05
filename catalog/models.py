# catalog/models.py
from django.db import models
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
import os


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
    description = models.TextField(blank=True, null=True, default='')
    image = models.ImageField(upload_to="products/", blank=True, null=True, default='images/products/default.png')
    created_at = models.DateTimeField(auto_now_add=True)
    specs = models.CharField(blank=True, null=True, default='')

    def __str__(self):
        return f"{self.brand.name} {self.name}" if self.brand else self.name
    

# Сигналы для работы с файлами
@receiver(post_delete, sender=Product)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            instance.image.delete(save=False)

@receiver(pre_save, sender=Product)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return
    
    try:
        old_file = Product.objects.get(pk=instance.pk).image
    except Product.DoesNotExist:
        return
    
    new_file = instance.image
    if old_file and old_file != new_file:
        if os.path.isfile(old_file.path):
            old_file.delete(save=False)