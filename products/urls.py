from django.urls import path
from .views import product_list, product_detail, category_list

urlpatterns = [
    path('', product_list, name='product_list'),
    path('category/<slug:slug>/', category_list, name='category_list'),
    path('<slug:slug>/', product_detail, name='product_detail'),
]
