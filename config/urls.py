from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from orders.views import pay_on_delivery, pay_on_livraison 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('products/', include('products.urls')),
    path('cart/', include('cart.urls')),
    path('orders/', include('orders.urls')),
    path('cart/pay-on-delivery/', pay_on_delivery, name='pay_on_delivery'),
    path('cart/pay-on-livraison/', pay_on_livraison, name='pay_on_livraison'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



