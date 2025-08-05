from django.shortcuts import render, get_object_or_404
from .models import Product, Category, Brand
from django.db.models import Count
from django.db.models import Q

# catalog/views.py
def product_list(request, category_slug=None, brand_slug=None):
    # Получаем категории с количеством товаров
    categories = Category.objects.annotate(
        product_count=Count('product', distinct=True)
    )
    
    # Получаем бренды с количеством товаров
    brands = Brand.objects.annotate(
        product_count=Count('product', distinct=True)
    )
    
    # Базовый запрос товаров
    products = Product.objects.all().select_related('category', 'brand')
    
    # Определяем активные категорию и бренд
    active_category = None
    active_brand = None
    
    # Фильтрация по категории
    if category_slug:
        active_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=active_category)
    
    # Фильтрация по бренду
    if brand_slug:
        active_brand = get_object_or_404(Brand, slug=brand_slug)
        products = products.filter(brand=active_brand)
    
    context = {
        'active_category': active_category,
        'active_brand': active_brand,
        'categories': categories,
        'brands': brands,
        'products': products,
    }
    
    return render(request, 'catalog/product_list.html', context)

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    context = {
        'product': product,
        'title': f'{product.name} - Детали'
    }
    return render(request, 'catalog/product_detail.html', context)