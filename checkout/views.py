import json
import secrets
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from paypalcheckoutsdk.orders import OrdersGetRequest

from accounts.forms import UserAddressForm
from accounts.models import Address
from App.models import Product
from App_cart.cart import Cart
from orders.models import Order, OrderItem
from wallet.models import Transaction, Wallet

from .models import DeliveryOptions
from .paypal import PayPalClient


@login_required
def delivery_choices(request):
    cart = Cart(request)
    for product_id, item in list(cart.cart.items()):
        product = Product.objects.get(pk=product_id)
        if item["quantity"] > product.product_stock:
            messages.error(request, "Insufficient stock")
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

    delivery_options = DeliveryOptions.objects.filter(is_active=True)
    context = {"delivery_options": delivery_options}
    return render(request, "checkout/delivery_choices.html", context)


@login_required
def basket_update_delivery(request):
    cart = Cart(request)

    if request.POST.get("action") == "post":
        delivery_option = request.POST.get("delivery_option")
        delivery_type = DeliveryOptions.objects.get(id=delivery_option)
        updated_total_price = cart.cart_update_delivery(delivery_type.delivery_price)

        session = request.session
        if "purchase" not in request.session:
            session["purchase"] = {
                "delivery_id": delivery_type.id,
            }
        else:
            session["purchase"]["delivery_id"] = delivery_type.id
            session.modified = True

        response = JsonResponse(
            {
                "total": updated_total_price,
                "delivery_price": delivery_type.delivery_price,
            }
        )
        return response


@login_required
def delivery_address(request):
    cart = Cart(request)
    for product_id, item in list(cart.cart.items()):
        print(product_id, item)
        product = Product.objects.get(pk=product_id)
        if item["quantity"] > product.product_stock:
            messages.error(request, "Insufficient stock")
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

    session = request.session
    if "purchase" not in request.session:
        messages.error(request, "Please select a delivery option")
        return HttpResponseRedirect(request.META["HTTP_REFERER"])

    if request.method == "POST":
        form = UserAddressForm(request.POST)
        if form.is_valid():
            address_form = form.save(commit=False)
            address_form.customer = request.user
            addresses.default = True
            address_form.save()
            messages.success(request, "New address added")
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    else:
        form = UserAddressForm()

    addresses = Address.objects.filter(customer=request.user).order_by("-default")

    if addresses:
        if "address" not in request.session:
            session["address"] = {"address_id": str(addresses[0].id)}
        else:
            session["address"]["address_id"] = str(addresses[0].id)
            session.modified = True

    context = {"addresses": addresses, "form": form}
    return render(request, "checkout/delivery_address.html", context)


@login_required
def payment_selection(request):
    cart = Cart(request)
    for product_id, item in list(cart.cart.items()):
        print(product_id, item)
        product = Product.objects.get(pk=product_id)
        if item["quantity"] > product.product_stock:
            messages.error(request, "Insufficient stock")
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

    session = request.session
    if "address" not in request.session:
        messages.error(request, "Please select an address option")
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

    address = Address.objects.get(customer=request.user, default=True)

    context = {"address": address}
    return render(request, "checkout/payment_selection.html", context)


def generate_order_key():
    # Generate a random 16-character order key
    return secrets.token_hex(8).upper()


@login_required
def cod_payment_complete(request):
    cart = Cart(request)
    user = request.user
    address = Address.objects.get(customer=user, default=True)
    user_id = user.id
    full_name = address.full_name
    email = (address.email,)
    address1 = address.address_line
    address2 = address.address_line2
    postal_code = address.postcode
    order_status = Order.OrderStatus.PENDING
    delivery_price = cart.get_delivery_price()
    if cart.coupon:
        subtotal = cart.get_subtotal_price_after_discount()
    else:
        subtotal = cart.get_subtotal_price()
    total_paid = cart.get_total_price_with_tax()
    order_key = generate_order_key()
    if cart.coupon:
        coupon = cart.coupon
        discount = cart.coupon.discount
    else:
        coupon = None
        discount = Decimal(0)

    with transaction.atomic():
        order = Order.objects.create(
            user_id=user_id,
            full_name=full_name,
            email=email[0],
            address1=address1,
            address2=address2,
            postal_code=postal_code,
            delivery_price=delivery_price,
            subtotal=subtotal,
            total_paid=total_paid,
            order_key=order_key,
            payment_option="cod",
            order_status=order_status,
            coupon=coupon,
            discount=discount,
        )

        order_id = order.pk

        for item in cart:
            product = item["product"]
            price = item["price"]
            quantity = item["quantity"]

            OrderItem.objects.create(
                order_id=order_id,
                product=product,
                price=price,
                quantity=quantity,
            )

            # Decrease the product stock
            product.product_stock -= quantity
            product.save()

    cart.clear()

    return render(request, "checkout/payment_successful.html", {})


@login_required
def payment_complete(request):
    PPClient = PayPalClient()

    body = json.loads(request.body)
    data = body.get("orderID")  # Check if 'orderID' exists in the body
    user_id = request.user.id
    order_status = Order.OrderStatus.PAID

    request_order = OrdersGetRequest(data)
    response = PPClient.client.execute(request_order)

    # total_paid = response.result.purchase_units[0].amount.value

    cart = Cart(request)
    delivery_price = cart.get_delivery_price()
    if cart.coupon:
        subtotal = cart.get_subtotal_price_after_discount()
    else:
        subtotal = cart.get_subtotal_price()
    if cart.coupon:
        coupon = cart.coupon
        discount = cart.coupon.discount
    else:
        coupon = None
        discount = Decimal(0)

    total_paid = cart.get_total_price_with_tax()

    # Check if the necessary fields exist in the API response before accessing them
    # full_name = (
    #     response.result.purchase_units[0].shipping.name.full_name
    #     if hasattr(response.result.purchase_units[0].shipping.name, "full_name")
    #     else ""
    # )
    # email = (
    #     response.result.payer.email_address
    #     if hasattr(response.result.payer, "email_address")
    #     else ""
    # )
    # address1 = (
    #     response.result.purchase_units[0].shipping.address.address_line_1
    #     if hasattr(response.result.purchase_units[0].shipping.address, "address_line_1")
    #     else ""
    # )
    # address2 = (
    #     response.result.purchase_units[0].shipping.address.admin_area_2
    #     if hasattr(response.result.purchase_units[0].shipping.address, "admin_area_2")
    #     else ""
    # )
    # postal_code = (
    #     response.result.purchase_units[0].shipping.address.postal_code
    #     if hasattr(response.result.purchase_units[0].shipping.address, "postal_code")
    #     else ""
    # )
    # country_code = (
    #     response.result.purchase_units[0].shipping.address.country_code
    #     if hasattr(response.result.purchase_units[0].shipping.address, "country_code")
    #     else ""
    # )

    user_address = Address.objects.filter(customer=request.user, default=True).first()

    with transaction.atomic():
        order = Order.objects.create(
            user_id=user_id,
            full_name=user_address.full_name,
            email=user_address.email,
            address1=user_address.address_line,
            address2=user_address.address_line2,
            postal_code=user_address.postcode,
            city=user_address.town_city,
            delivery_price=delivery_price,
            subtotal=subtotal,
            total_paid=total_paid,
            order_key=response.result.id,
            payment_option="paypal",
            billing_status=True,
            order_status=order_status,
            coupon=coupon,
            discount=discount,
        )

        order_id = order.pk

        for item in cart:
            product = item["product"]
            price = item["price"]
            quantity = item["quantity"]

            OrderItem.objects.create(
                order_id=order_id,
                product=product,
                price=price,
                quantity=quantity,
            )

            # Decrease the product stock
            product.product_stock -= quantity
            product.save()

    return JsonResponse("Payment Completed!", safe=False)


@login_required
def wallet_payment_complete(request):
    cart = Cart(request)
    user = request.user
    address = Address.objects.get(customer=user, default=True)
    user_id = user.id
    full_name = address.full_name
    email = (address.email,)
    address1 = address.address_line
    address2 = address.address_line2
    postal_code = address.postcode
    delivery_price = cart.get_delivery_price()
    order_status = Order.OrderStatus.PAID
    total_paid = cart.get_total_price_with_tax()
    order_key = generate_order_key()
    if cart.coupon:
        coupon = cart.coupon
        discount = cart.coupon.discount
        subtotal = cart.get_subtotal_price_after_discount()
    else:
        coupon = None
        discount = Decimal(0)
        subtotal = cart.get_subtotal_price()

    with transaction.atomic():
        wallet = Wallet.objects.get(user=user)

        if wallet.balance >= total_paid:
            order = Order.objects.create(
                user_id=user_id,
                full_name=full_name,
                email=email[0],
                address1=address1,
                address2=address2,
                postal_code=postal_code,
                delivery_price=delivery_price,
                subtotal=subtotal,
                total_paid=total_paid,
                order_key=order_key,
                payment_option="wallet",
                order_status=order_status,
                coupon=coupon,
                discount=discount,
            )
            wallet.balance -= order.total_paid
            wallet.save()

            Transaction.objects.create(
                user=user,
                transaction_type=Transaction.TransactionTypes.PURCHASE,
                amount=order.total_paid,
            )

            order_id = order.pk

            for item in cart:
                product = item["product"]
                price = item["price"]
                quantity = item["quantity"]

                OrderItem.objects.create(
                    order_id=order_id,
                    product=product,
                    price=price,
                    quantity=quantity,
                )

                # Decrease the product stock
                product.product_stock -= quantity
                product.save()

        else:
            messages.error(request, "Insufficient balance in your wallet.")
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

    cart.clear()

    return render(request, "checkout/payment_successful.html", {})


@login_required
def payment_successful(request):
    cart = Cart(request)
    cart.clear()
    return render(request, "checkout/payment_successful.html", {})
