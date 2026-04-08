from django.urls import path
from .views import contact, faq, shipping_returns, subscribe_newsletter

urlpatterns = [
    path('contact/', contact, name='contact'),
    path('faq/', faq, name='faq'),
    path('shipping-returns/', shipping_returns, name='shipping_returns'),
    path('subscribe/', subscribe_newsletter, name='subscribe_newsletter'),
]
