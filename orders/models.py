# orders/models.py
from django.db import models
from products.models import Product  # <-- à adapter selon où se trouve ton modèle Product



class Order(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ("pending", "En attente"),
        ("paid", "Payé"),
        ("failed", "Échoué"),
    ]

    PAYMENT_METHOD_CHOICES = [
        ("qr_code", "QR Code"),
        ("cash", "Paiement à la livraison"),
        ("default", "Par défaut"),
    ]

    # Infos client
    first_name = models.CharField("Prénom", max_length=100)
    last_name = models.CharField("Nom", max_length=100)
    email = models.EmailField("Email")
    address = models.CharField("Adresse", max_length=250)
    phone = models.CharField("Téléphone", max_length=20)

    # Paiement
    payment_method = models.CharField(
        "Méthode de paiement",
        max_length=50,
        choices=PAYMENT_METHOD_CHOICES,
        default="default"
    )
    payment_status = models.CharField(
        "Statut du paiement",
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default="pending"
    )

    total_amount = models.DecimalField(
        "Total de la commande",
        max_digits=10,
        decimal_places=2,
        default=0
    )

    created_at = models.DateTimeField("Date de création", auto_now_add=True)

    def save(self, *args, **kwargs):
        # Si payé par QR Code, alors statut = payé
        if self.payment_method == "qr_code":
            self.payment_status = "paid"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Commande {self.id} - {self.first_name} {self.last_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # <--- lien direct au produit
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # prix unitaire au moment de la commande

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

