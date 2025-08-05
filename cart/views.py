from django.shortcuts import render, redirect, get_object_or_404
from catalog.models import Product
from django.views.decorators.http import require_POST

def cart_add(request, product_id):
    # Инициализация корзины в сессии
    if 'cart' not in request.session:
        request.session['cart'] = {}
    
    # Обновление количества
    cart = request.session['cart']
    product_key = str(product_id)
    cart[product_key] = cart.get(product_key, 0) + 1
    
    # Принудительное сохранение сессии
    request.session.modified = True
    
    return redirect('catalog:product_list')

def cart_view(request):
    cart = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart.keys())
    cart_items = []
    for product in products:
        cart_items.append({
            'product': product,
            'quantity': cart[str(product.id)],
            'total': product.price * cart[str(product.id)]
        })
    return render(request, 'cart/cart.html', {'cart_items': cart_items})

def cart_remove(request, product_id):
    """Удаление товара из корзины"""
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})
    
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart
        request.session.modified = True
    
    return redirect('cart:cart_view')

@require_POST
def cart_update(request):
    if request.user.is_authenticated:
        # Для авторизованных пользователей
        cart = Cart.objects.get(user=request.user)
        for item in cart.items.all():
            new_quantity = int(request.POST.get(f'quantity_{item.product.id}', item.quantity))
            item.quantity = new_quantity
            item.save()
    else:
        # Для гостей (сессия)
        cart = request.session.get('cart', {})
        for product_id, quantity in cart.items():
            new_quantity = int(request.POST.get(f'quantity_{product_id}', quantity))
            cart[product_id] = new_quantity
        request.session['cart'] = cart
    
    return redirect('cart:cart_view')