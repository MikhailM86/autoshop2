from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from cart.models import Cart
from .models import Order

@login_required
def checkout(request):
    cart = Cart.objects.get(user=request.user)
    
    if request.method == 'POST':
        # Временная логика - сохраняем заказ без формы
        order = Order.objects.create(
            user=request.user,
            cart=cart,
            shipping_address=request.POST.get('address'),
            phone=request.POST.get('phone'),
        )
        return redirect('order_success', order_id=order.id)
    
    return render(request, 'orders/checkout.html', {'cart': cart})