from django.contrib import admin

from .models import Coupon, DeliveryOptions

admin.site.register(DeliveryOptions)
admin.site.register(Coupon)
