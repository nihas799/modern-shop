from django.urls import path
from .views import *

urlpatterns = [
    path('checkout/', checkout, name='checkout'),
     path('success/', order_success, name='order_success'),
    path('my-orders/', my_orders, name='my_orders'),
    path('cancel/<int:order_id>/',cancel_order, name='cancel_order'),
    path('payment-success/',payment_success, name='payment_success'),


]
