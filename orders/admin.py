from django.contrib import admin
from django.utils.html import format_html
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'first_name', 'last_name', 'email', 'address', 'phone',
        'display_products', 'total_price', 'payment_status_badge', 'created_at'
    )
    inlines = [OrderItemInline]

    def display_products(self, obj):
        if not obj.items.exists():
            return "-"
        html = "<table style='border-collapse: collapse;'>"
        html += "<tr><th style='border:1px solid #ccc; padding:3px;'>Produit</th><th style='border:1px solid #ccc; padding:3px;'>Qté</th><th style='border:1px solid #ccc; padding:3px;'>Prix</th></tr>"
        for item in obj.items.all():
            html += f"<tr><td style='border:1px solid #ccc; padding:3px;'>{item.product.name}</td>"
            html += f"<td style='border:1px solid #ccc; padding:3px; text-align:center;'>{item.quantity}</td>"
            html += f"<td style='border:1px solid #ccc; padding:3px;'>{item.product.price * item.quantity} FCFA</td></tr>"
        html += "</table>"
        return format_html(html)
    display_products.short_description = 'Produits commandés'

    def total_price(self, obj):
        return sum([item.product.price * item.quantity for item in obj.items.all()])
    total_price.short_description = 'Prix total'

    def payment_status_badge(self, obj):
        if obj.payment_status == "paid":
            color, label = "green", "Payé"
        elif obj.payment_status == "pending":
            color, label = "orange", "En attente"
        else:
            color, label = "red", "Échoué"
        return format_html(f"<span style='color:white; background:{color}; padding:3px 8px; border-radius:5px;'>{label}</span>")
    payment_status_badge.short_description = "Statut paiement"
