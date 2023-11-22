from accounts.models import Customer
from orders.models import Invoice, Order
from django.http import HttpRequest

from .models import Category, Product


def categories(request):
    return {
        "categories": Category.objects.filter(is_active=True, level=0),
    }


def user_wishlist(request):
    try:
        if request.user.is_authenticated:
            return {
                "user_wishlist": Product.objects.filter(user_wishlist=request.user),
            }
        else:
            return []
    except:
        return []


def orders_count(request):
    orders_count = Order.objects.all().count()  # Retrieve the count of all orders
    customers_count = Customer.objects.all().count()
    invoices_count = Invoice.objects.all().count()
    return {
        "orders_count": orders_count,
        "customers_count": customers_count,
        "invoices_count": invoices_count,
    }
