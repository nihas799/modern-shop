from django.urls import path
from .views import *

urlpatterns = [
    path("", product_list, name="product_list"),
    path("category/<slug:category_slug>/", product_list, name="category_filter"),
    path("product/<slug:slug>/", product_detail, name="product_detail"),
    path('wishlist/', wishlist, name='wishlist'),
    path('wishlist/add/<int:product_id>/', add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>/', remove_from_wishlist, name='remove_from_wishlist'),
    path('buy-now/<int:product_id>/', buy_now, name='buy_now'),
    path('search/', search_view, name='search'),
    path('search-suggestions/', search_suggestions, name='search_suggestions'),

]
