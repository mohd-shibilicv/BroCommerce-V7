import json

from django.contrib import messages
from django.core.serializers import serialize
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from App.models import Product
from checkout.forms import CouponForm
from checkout.models import Coupon

from .cart import Cart


def view_cart(request):
    context = {"coupon_form": CouponForm()}
    return render(request, "App_cart/cart.html", context)


def add_to_cart(request):
    cart = Cart(request)
    if request.POST.get("action") == "post":
        product_id = int(request.POST.get("productid"))
        product_quantity = int(request.POST.get("productquantity"))
        product = get_object_or_404(Product, id=product_id)
        cart.add(product=product, productquantity=product_quantity)

        cart_quantity = cart.__len__()
        response = JsonResponse({"quantity": cart_quantity})
        return response


@require_POST
def coupon_apply(request):
    now = timezone.now()
    form = CouponForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data["code"]
        try:
            coupon = Coupon.objects.get(
                code__iexact=code, valid_from__lte=now, valid_to__gte=now, active=True
            )
            request.session["coupon_id"] = coupon.id
        except Coupon.DoesNotExist:
            messages.error(request, "Invalid coupon")
            return HttpResponseRedirect(request.META["HTTP_REFERER"])
    return redirect("cart:view_cart")


def get_available_coupons(request):
    coupons_queryset = Coupon.objects.filter(
        user=request.user,
        active=True,
        valid_from__lte=timezone.now(),
        valid_to__gte=timezone.now(),
    )
    coupons_json = serialize('json', coupons_queryset)
    coupons_list = json.loads(coupons_json)

    coupons = [{'code': coupon['fields']['code'], 'discount': coupon['fields']['discount']} for coupon in coupons_list]

    return JsonResponse(coupons, safe=False)


def cart_delete(request):
    cart = Cart(request)
    if request.POST.get("action") == "post":
        product_id = int(request.POST.get("productid"))
        cart.delete(product=product_id)
        cart_quantity = cart.__len__()
        cart_total = cart.get_total_price()
        response = JsonResponse({"quantity": cart_quantity, "subtotal": cart_total})
        return response


def cart_update(request):
    cart = Cart(request)
    if request.POST.get("action") == "post":
        product_id = int(request.POST.get("productid"))
        product_quantity = int(request.POST.get("productquantity"))

        cart.update(product=product_id, quantity=product_quantity)

        cart_quantity = cart.__len__()
        cart_subtotal = cart.get_subtotal_price()
        cart_total = cart.get_total_price()
        productquantity = product_quantity
        response = JsonResponse(
            {
                "quantity": cart_quantity,
                "total": cart_total,
                "subtotal": cart_subtotal,
                "productquantity": productquantity,
            }
        )
        return response
