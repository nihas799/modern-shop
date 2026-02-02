from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, Wishlist
from cart.cart import Cart


def product_list(request, category_slug=None):
    categories = Category.objects.all()
    products = Product.objects.filter(is_available=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    else:
        category = None

    context = {
        "products": products,
        "categories": categories,
        "current_category": category,
    }
    return render(request, "product_list.html", context)

from django.shortcuts import render, get_object_or_404
from .models import Product, Category


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_available=True)
    categories = Category.objects.all()

    context = {
        "product": product,
        "categories": categories,
    }
    return render(request, "product_detail.html", context)


@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Wishlist.objects.get_or_create(user=request.user, product=product)
    return redirect('wishlist')

@login_required
def wishlist(request):
    items = Wishlist.objects.filter(user=request.user)
    return render(request, 'wishlist.html', {'items': items})

@login_required
def remove_from_wishlist(request, product_id):
    Wishlist.objects.filter(user=request.user, product_id=product_id).delete()
    return redirect('wishlist')
@login_required
def buy_now(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart = Cart(request)
    cart.clear()  # remove existing cart items

    cart.add(
        product=product,
        quantity=1,

    )

    return redirect('checkout')