from django.urls import path

from . import views

app_name = "cart"

urlpatterns = [
    path("", views.view_cart, name="view_cart"),
    path("coupon_apply/", views.coupon_apply, name="coupon_apply"),
    path('get_available_coupons/', views.get_available_coupons, name='get_available_coupons'),
    path("add/", views.add_to_cart, name="add_to_cart"),
    path("delete/", views.cart_delete, name="cart_delete"),
    path("update/", views.cart_update, name="cart_update"),
]
