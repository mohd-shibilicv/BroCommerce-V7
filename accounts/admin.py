from django.contrib import admin

from .models import Address, Customer, Referral

admin.site.register(Customer)
admin.site.register(Address)
admin.site.register(Referral)
