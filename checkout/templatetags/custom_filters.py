from decimal import Decimal

from django import template

from checkout.models import Coupon

register = template.Library()


@register.filter(name="apply_coupon")
def apply_coupon(total_price, coupon_code):
    try:
        coupon = Coupon.objects.get(code=coupon_code)
        discount = Decimal(coupon.discount_percentage) / Decimal(100)
        return total_price * discount
    except Coupon.DoesNotExist:
        return total_price
