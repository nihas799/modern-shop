from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from .models import Order, OrderItem
from decimal import Decimal
from django.contrib import messages


@login_required
def checkout(request):
    cart = Cart(request)

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')

        if not payment_method:
            messages.error(request, "Please select a payment method.")
            return redirect('checkout')

        order = Order.objects.create(
            user=request.user,
            full_name=request.POST.get('full_name'),
            phone=request.POST.get('phone'),
            address_line=request.POST.get('address_line'),
            city=request.POST.get('city'),
            post_office=request.POST.get('post_office'),
            state=request.POST.get('state'),
            pincode=request.POST.get('pincode'),
            total_price=cart.get_total_price(),
            payment_method=request.POST.get('payment_method'),
            payment_status='PENDING',
            status='PENDING'
        )

        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                price=item['price'],
                quantity=item['quantity']
            )

        cart.clear()

        if payment_method == 'ONLINE':
            return redirect('payment_success')

        return redirect('order_success')

    return render(request, 'checkout.html')

from django.shortcuts import render

from django.shortcuts import render

def order_success(request):
    return render(request, 'order_success.html')

def payment_success(request):
    return render(request, 'payment_success.html')
    order.payment_status = 'PAID'
    order.status = 'CONFIRMED'
    order.save()

    send_order_confirmation(order)

def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'my_orders.html', {'orders': orders})
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if order.status != 'PENDING':
        messages.error(request, "This order can no longer be cancelled.")
        return redirect('my_orders')

    if request.method == 'POST':
        reason = request.POST.get('reason')

        if not reason:
            messages.error(request, "Please provide a cancellation reason.")
            return redirect('cancel_order', order_id=order.id)

        order.status = 'CANCELLED'
        order.cancel_reason = reason
        order.save()
        from .utils import send_order_confirmation

        send_order_confirmation(order)

        messages.success(request, "Your order has been cancelled.")
        return redirect('my_orders')

    return render(request, 'cancel_order.html', {'order': order})