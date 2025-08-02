from .models import Cart

def cart_items_count(request):
    count = 0
    if hasattr(request, 'user') and request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        count = cart.items.count() if cart else 0
    return {'cart_items_count': count}