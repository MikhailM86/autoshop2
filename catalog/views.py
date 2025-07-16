from django.shortcuts import render
from .models import Product
from .models import Category
from .models import Brand
from django.db.models import Q

def product_list(request):
    category = request.GET.get('category')
    brand = request.GET.get('brand')
    
    products = Product.objects.all()
    
    if category:
        products = products.filter(category__slug=category)
    if brand:
        products = products.filter(brand__slug=brand)
        
    return render(request, 'catalog/product_list.html', {
        'products': products,
        'categories': Category.objects.all(),
        'brands': Brand.objects.all()
    })

def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    return render(request, "catalog/product_detail.html", {"product": product})