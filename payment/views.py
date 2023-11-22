from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm

from App_cart.cart import Cart


@login_required
def checkout_view(request):
    host = request.get_host()

    paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": "200",
        "item_name": "Order_item_number-2",
        "invoice": "invoice_id_3",
        "currency_code": "INR",
        "notify_url": "http://{}{}".format(host, reverse("paypal-ipn")),
        "return_url": "http://{}{}".format(host, reverse("payment:payment_completed")),
        "cancel_url": "http://{}{}".format(host, reverse("payment:payment_failed")),
    }

    paypal_payment_button = PayPalPaymentsForm(initial=paypal_dict)

    context = {"paypal_payment_button": paypal_payment_button}
    return render(request, "payment/checkout.html", context)


def order_placed(request):
    cart = Cart(request)
    cart.clear()
    return render(request, "payment/orderplaced.html")


@csrf_exempt
def payment_failed_view(request):
    return render(request, "payment/payment_failed.html")


@csrf_exempt
def payment_completed_view(request):
    return render(request, "payment/payment_completed.html")
