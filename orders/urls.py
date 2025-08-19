from django.urls import path
from . import views  # OK ici, car views.py existe dans orders

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('success/', views.success, name='success'),
    path('pay-on-delivery/', views.pay_on_delivery, name='pay_on_delivery'),
    path('pay-on-livraison/', views.pay_on_livraison, name='pay_on_livraison'),
    path('checkout/wave/', views.wave_payment, name='wave_payment'),
]
