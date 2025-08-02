from django.db import models
from users.models import User
from cart.models import Cart

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'В обработке'),
        ('completed', 'Завершен'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    shipping_address = models.TextField()
    phone = models.CharField(max_length=20)

    def __str__(self):
        return f"Заказ #{self.id} - {self.user.username}"

    def total_price(self):
        return sum(item.total_price() for item in self.cart.cartitem_set.all())