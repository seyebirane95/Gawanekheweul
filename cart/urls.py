from django.urls import path
from .views import add_to_cart, remove_from_cart, view_cart, clear_cart, update_quantity

urlpatterns = [
    path('', view_cart, name='view_cart'),
    path('add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('remove/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('update/<int:product_id>/', update_quantity, name='update_quantity'),
    path('clear/', clear_cart, name='clear_cart'),
]
