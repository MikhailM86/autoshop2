# catalog/models.py
from django.db import models
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
import os
from django.utils.text import slugify
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.conf import settings


class Brand(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to="brands/", blank=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

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
    slug = models.SlugField(max_length=200, blank=True, unique=True)
    part_number = models.CharField(max_length=50)  # Уникальный артикул
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True, null=True, default='')
    image = models.ImageField(
        upload_to="products/",
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    specs = models.CharField(blank=True, null=True, default='')

    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        return f"{settings.STATIC_URL}images/products/default.png"

    def __str__(self):
        return f"{self.brand.name} {self.name}" if self.brand else self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            counter = 1
        while Product.objects.filter(slug=self.slug).exclude(id=self.id).exists():
            self.slug = f"{slugify(self.name)}-{counter}"
            counter += 1
        super().save(*args, **kwargs)


def get_absolute_url(self):
    if not self.slug:  # Если slug ещё не создан
        self.save()    # Вызовет метод save() для генерации slug
    return reverse('product_detail', args=[self.id, self.slug])

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
