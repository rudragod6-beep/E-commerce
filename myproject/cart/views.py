from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product


# GET CART FROM SESSION
def get_cart(request):
    return request.session.get('cart', {})


# SAVE CART TO SESSION
def save_cart(request, cart):
    request.session['cart'] = cart
    request.session.modified = True


# ADD TO CART
def add_to_cart(request, id):
    product = get_object_or_404(Product, id=id)
    cart = get_cart(request)

    if str(id) in cart:
        cart[str(id)] += 1
    else:
        cart[str(id)] = 1

    save_cart(request, cart)
    return redirect('cart')


# REMOVE FROM CART
def remove_from_cart(request, id):
    cart = get_cart(request)

    if str(id) in cart:
        del cart[str(id)]

    save_cart(request, cart)
    return redirect('cart')


# CART PAGE
def cart_view(request):
    cart = get_cart(request)

    products = []
    total = 0

    for id, qty in cart.items():
        product = get_object_or_404(Product, id=id)
        product.qty = qty
        product.subtotal = product.price * qty

        total += product.subtotal
        products.append(product)

    return render(request, 'cart/cart.html', {
        'products': products,
        'total': total
    })