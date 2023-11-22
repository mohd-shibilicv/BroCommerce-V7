from django.urls import path

from . import views

app_name = "payment"

urlpatterns = [
    path("", views.checkout_view, name="checkout"),
    path("orderplaced/", views.order_placed, name="order_placed"),
    path("payment_completed/", views.payment_completed_view, name="payment_completed"),
    path("payment_failed/", views.payment_failed_view, name="payment_failed"),
]
