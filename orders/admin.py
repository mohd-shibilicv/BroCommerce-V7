from django.contrib import admin

from .models import Invoice, Order, OrderItem, OrderReturn

admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(OrderReturn)
admin.site.register(Invoice)
