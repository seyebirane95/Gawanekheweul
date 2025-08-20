from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from products.models import Product
from .models import Order, OrderItem  # si tu veux créer des commandes réelles

# --- Gestion du panier ---
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

# --- Checkout classique ---
def checkout(request):
    cart = request.session.get('cart', {})
    total = sum(item['price'] * item['qty'] for item in cart.values())

    if request.method == "POST":
        # récupérer infos du formulaire
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        email = request.POST.get('email')

        if not cart:
            messages.error(request, "Votre panier est vide.")
            return redirect('product_list')

        # Calculer total_amount
        total_amount = sum(item['price'] * item['qty'] for item in cart.values())

        # Créer la commande
        order = Order.objects.create(
            first_name=first_name,
            last_name=last_name,
            address=address,
            phone=phone,
            email=email,
            payment_method="qr_code",
            total_amount=total_amount
        )

        # Créer les items
        for pid, item in cart.items():
            OrderItem.objects.create(
                order=order,
                product_id=int(pid),
                quantity=item['qty'],
                price=item['price']
            )

        # vider le panier
        request.session['cart'] = {}
        request.session.modified = True

        # rediriger vers le paiement QR code
        return redirect('wave_payment', order_id=order.id)

    return render(request, 'orders/checkout.html', {
        'cart': cart,
        'total': total
    })


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Order, OrderItem

def wave_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        # Ici, le client confirme qu'il a payé
        order.payment_status = "paid"  # On marque la commande comme payée
        order.save()

        # Vider le panier
        request.session['cart'] = {}
        request.session.modified = True

        # Rediriger vers page de succès
        return redirect('success')

    qr_code_url = '/static/img/wave_qr.png'
    return render(request, 'commandes/paiement_vague.html', {
        'order': order,
        'qr_code_url': qr_code_url
    })



# --- Paiement après livraison ---
def pay_on_delivery(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.info(request, "Votre panier est vide.")
        return redirect('view_cart')

    if request.method == 'POST':
        # Récupération des infos client depuis le formulaire
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address', '')
        phone = request.POST.get('phone', '')

        total = sum(item['qty'] * float(item['price']) for item in cart.values())

        # Création de la commande
        order = Order.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            address=address,
            phone=phone,
            total_amount=total,
            status='pending'  # Assurez-vous que le champ status existe dans Order
        )

        # Création des OrderItem
        for pid, item in cart.items():
            product = Product.objects.get(id=pid)
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item['qty'],
                price=item['price']
            )

        # Vider le panier après création de la commande
        request.session['cart'] = {}
        request.session.modified = True

        messages.success(request, "Votre commande a été passée avec succès. Vous payerez à la livraison.")
        return redirect('success')  # page de confirmation
    total = sum(item['qty'] * item['price'] for item in cart.values())
    return render(request, 'orders/checkout.html', {
        'cart': cart,
        'total': total
    })
    #return render(request, 'orders/checkout.html', {'cart': cart})


def success(request):
    return render(request, 'orders/success.html')



def pay_on_livraison(request):
    cart = request.session.get('cart', {})

    if not cart:
        messages.info(request, "Votre panier est vide.")
        return redirect('view_cart')

    total = sum(item['qty'] * float(item['price']) for item in cart.values())

    if request.method == "POST":
        # récupérer infos du formulaire
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        phone = request.POST.get('phone')

        # créer la commande
        order = Order.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            address=address,
            phone=phone,
            payment_method="cash",  # paiement à la livraison
            payment_status="pending",  # pas encore payé
            total_amount=total
        )

        # ajouter les produits commandés
        for pid, item in cart.items():
            OrderItem.objects.create(
                order=order,
                product_id=int(pid),
                quantity=item['qty'],
                price=item['price']
            )

        # vider le panier
        request.session['cart'] = {}
        request.session.modified = True

        # rediriger vers page succès
        return redirect('success')

    return render(request, 'orders/pay_on_delivery.html', {
        'cart': cart,
        'total': total
    })
