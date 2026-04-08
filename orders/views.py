from django.dispatch import receiver
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from cart.models import Cart, CartItem
from .models import Order, OrderItem
from decimal import Decimal
from django.contrib import messages
from products.models import Product
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse


import razorpay
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from cart.models import Cart
from .models import Order, OrderItem, Payment

def send_order_email(order):
    subject = "Order Confirmed - ModernShop"

    message = f"""
Hello {order.full_name},

Your order has been placed successfully!

Order Details:
Order ID: {order.id}
Total Amount: ₹{order.total_price}

Thank you for shopping with ModernShop!
"""

    recipient_list = [order.user.email]

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        recipient_list,
        fail_silently=False
    )
def checkout(request):
    cart = Cart.objects.get(user=request.user)
    items = cart.items.all()

    if not items:
        messages.error(request, "Your cart is empty.")
        return redirect('cart_detail')

    total_price = cart.total_price()

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')

        # CREATE ORDER
        order = Order.objects.create(
            user=request.user,
            full_name=request.POST.get('full_name'),
            phone=request.POST.get('phone'),
            address_line=request.POST.get('address_line'),
            city=request.POST.get('city'),
            post_office=request.POST.get('post_office'),
            state=request.POST.get('state'),
            pincode=request.POST.get('pincode'),
            total_price=total_price,
            payment_method=payment_method,
            payment_status='PENDING',
            status='PENDING'
        )

        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                price=item.product.price,
                quantity=item.quantity
            )

        # 🟢 COD FLOW
        if payment_method == "cod":
            cart.items.all().delete()
            send_order_email(order)
            return redirect('order_success')

        # 🔵 ONLINE PAYMENT (RAZORPAY)
        elif payment_method == "online":
            client = razorpay.Client(
                auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
            )

            razorpay_order = client.order.create({
                "amount": int(total_price * 100),  # ₹ → paise
                "currency": "INR",
                "payment_capture": "1"
            })

            # SAVE PAYMENT
            payment = Payment.objects.create(
                user=request.user,
                order=order,
                razorpay_order_id=razorpay_order['id'],
                amount=razorpay_order['amount'],
                status="CREATED"
            )

            return render(request, "payment.html", {
                "payment": payment,
                "order": order,
                "razorpay_key": settings.RAZORPAY_KEY_ID
            })

    return render(request, 'checkout.html', {
        'items': items,
        'total_price': total_price
    })

from django.shortcuts import render

from django.shortcuts import render

def order_success(request):
    return render(request, 'order_success.html')

def payment_success(request):
    payment_id = request.GET.get('payment_id')
    order_id = request.GET.get('order_id')

    if not payment_id or not order_id:
        return redirect('checkout')

    try:
        payment = Payment.objects.get(razorpay_order_id=order_id)
    except Payment.DoesNotExist:
        return redirect('checkout')

    # SAVE PAYMENT ID
    payment.razorpay_payment_id = payment_id
    payment.status = "SUCCESS"
    payment.save()

    # UPDATE ORDER
    order = payment.order
    order.payment_status = 'PAID'
    order.status = 'CONFIRMED'
    order.save()

    # CLEAR CART
    Cart.objects.get(user=request.user).items.all().delete()

    # EMAIL
    from .utils import send_order_confirmation
    send_order_email(order)

    return render(request, 'payment_success.html', {'order': order})
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