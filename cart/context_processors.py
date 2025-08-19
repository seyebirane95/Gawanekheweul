def cart(request):
    cart = request.session.get('cart', {})
    total_qty = sum(item['qty'] for item in cart.values())
    total_price = sum(item['qty'] * float(item['price']) for item in cart.values())
    return {'cart_total_qty': total_qty, 'cart_total_price': total_price}
