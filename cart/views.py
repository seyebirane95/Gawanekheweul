from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from products.models import Product

def _get_cart(session):
    return session.setdefault('cart', {})

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id, is_active=True)
    cart = _get_cart(request.session)
    item = cart.get(str(product_id), {'name': product.name, 'price': float(product.price), 'qty': 0})
    if product.stock <= item['qty']:
        messages.warning(request, "Stock insuffisant.")
    else:
        item['qty'] += 1
        cart[str(product_id)] = item
        request.session.modified = True
        messages.success(request, f"{product.name} ajouté au panier.")
    return redirect('product_detail', slug=product.slug)

def remove_from_cart(request, product_id):
    cart = _get_cart(request.session)
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session.modified = True
        messages.info(request, "Article retiré du panier.")
    return redirect('view_cart')

def update_quantity(request, product_id):
    qty = int(request.POST.get('qty', 1))
    cart = _get_cart(request.session)
    if str(product_id) in cart:
        cart[str(product_id)]['qty'] = max(1, qty)
        request.session.modified = True
    return redirect('view_cart')

def clear_cart(request):
    request.session['cart'] = {}
    request.session.modified = True
    messages.info(request, "Panier vidé.")
    return redirect('view_cart')

def view_cart(request):
    cart = request.session.get('cart', {})
    return render(request, 'cart/view.html', {'cart': cart})

def pay_on_delivery(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.info(request, "Votre panier est vide.")
        return redirect('view_cart')  # reste sur la page du panier

    # Vider le panier pour simuler la validation de commande
    request.session['cart'] = {}
    request.session.modified = True

    # Rediriger vers la page de succès
    return redirect('success')  # '/orders/success/'