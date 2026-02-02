from django.urls import path
from .views import product_list, product_detail, remove_from_wishlist, add_to_wishlist, wishlist, buy_now

urlpatterns = [
    path("", product_list, name="product_list"),
    path("category/<slug:category_slug>/", product_list, name="category_filter"),
    path("product/<slug:slug>/", product_detail, name="product_detail"),
    path('wishlist/', wishlist, name='wishlist'),
    path('wishlist/add/<int:product_id>/', add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>/', remove_from_wishlist, name='remove_from_wishlist'),
    path('buy-now/<int:product_id>/', buy_now, name='buy_now'),

]
