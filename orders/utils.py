from django.core.mail import send_mail
from django.conf import settings

def send_order_confirmation(order):
    subject = f"Order #{order.id} Confirmed | ModernShop"

    message = f"""
Hi {order.full_name},

Thank you for shopping with ModernShop! 🛍️

🧾 Order ID: {order.id}
💰 Total Amount: ₹{order.total_price}
💳 Payment Method: {order.get_payment_method_display()}
📦 Order Status: {order.status}

📍 Delivery Address:
{order.address_line}
{order.post_office}, {order.city}
{order.state} - {order.pincode}

📞 Phone: {order.phone}

We’ll notify you when your order is shipped.

Thank you,
ModernShop Team
"""

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [order.user.email],
        fail_silently=False,
    )
