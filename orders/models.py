# orders/models.py
from django.db import models
from products.models import Product  # <-- à adapter selon où se trouve ton modèle Product

from django.db import models

class Order(models.Model):
    email = models.EmailField()
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='pending')  # <-- ajouté

    def __str__(self):
        return f"Commande {self.id} - {self.email}"



class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # <--- lien direct au produit
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # prix unitaire au moment de la commande

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

