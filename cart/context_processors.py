from .models import Cart

def cart_items_count(request):
    count = 0
    
    # Для анонимных пользователей (сессия)
    if 'cart' in request.session:
        count = sum(request.session['cart'].values())
    
    # Для авторизованных (БД)
    elif request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        count = cart.items.count() if cart else 0
    
    return {'cart_items_count': count}