from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from cart.views import get_cart, save_cart
from products.models import Product
from .models import Order, OrderItem


@login_required
def checkout(request):
    cart = get_cart(request)

    if not cart:
        return redirect('cart')

    total = 0
    cart_products = []

    for id, qty in cart.items():
        product = get_object_or_404(Product, id=id)
        product.qty = qty
        product.subtotal = product.price * qty

        total += product.subtotal
        cart_products.append(product)

    # CREATE ORDER
    order = Order.objects.create(
        user=request.user,
        total_price=total
    )

    # CREATE ORDER ITEMS
    for product in cart_products:
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=product.qty,
            price=product.price
        )
        # Decrement stock
        product.stock -= product.qty
        product.save()

    # CLEAR CART
    save_cart(request, {})

    return redirect('success')


def success(request):
    return render(request, 'order/success.html')


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'order/my_orders.html', {'orders': orders})


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'orders/my_orders.html', {
        'orders': orders
    })