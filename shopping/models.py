from django.db import models
from user.models import User
from products.models import Product, BargainOffer


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}'s Cart"

class CartItem(models.Model):
    cart: Cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def price(self):
        bargain: BargainOffer = self.product.bargainoffer_set.filter(buyer=self.cart.user, is_accepted=True).order_by(
            "-accepted_at").first()
        return bargain.offer_price if bargain else self.product.price

    def subtotal(self):
        return self.price() * self.quantity

class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    PAYMENT_METHODS = [
        ('Stripe', 'Stripe'),
        ('bKash', 'bKash'),
        ('Nagad', 'Nagad'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.TextField(max_length= 1000, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    payment_completed = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
