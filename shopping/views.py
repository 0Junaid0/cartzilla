from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, CartItem, Order, OrderItem
from products.models import Product
from django.contrib.auth.decorators import login_required
from django.contrib import messages
#from decimal import Decimal

@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    total = sum([item.subtotal() for item in cart_items])
    return render(request, 'shopping/cart.html', {'cart_items': cart_items, 'total': total})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, f'Added {product.name} to cart!')
    return redirect('cart')

@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.delete()
    messages.success(request, 'Item removed from cart.')
    return redirect('cart')

@login_required
def checkout_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    total = sum([item.subtotal() for item in cart_items])

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        address = request.POST.get('address')
        order = Order.objects.create(
            user=request.user,
            total_price=total,
            payment_method=payment_method,
            address = address,
            payment_completed=True,  # simulate payment success
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
            )

        cart_items.delete()  # Clear cart
        messages.success(request, 'Order placed successfully!')
        return redirect('payment_success')

    return render(request, 'shopping/checkout.html', {'cart_items': cart_items, 'total': total})

@login_required
def order_history_view(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    return render(request, 'shopping/order_history.html', {'orders': orders})

@login_required
def payment_success_view(request):
    return render(request, 'shopping/payment_success.html')
