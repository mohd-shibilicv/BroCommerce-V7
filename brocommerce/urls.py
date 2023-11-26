import debug_toolbar
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("admin/", admin.site.urls),
    path("shopadmin/", include("shopadmin.urls", namespace="shopadmin")),
    path("__debug__/", include(debug_toolbar.urls)),
    path("", include("home.urls", namespace="home")),
    path("accounts/", include("allauth.urls")),
    path("shop/", include("App.urls", namespace="App")),
    path("cart/", include("App_cart.urls", namespace="cart")),
    path("account/", include("accounts.urls", namespace="account")),
    path("checkout/", include("checkout.urls", namespace="checkout")),
    path("payment/", include("payment.urls", namespace="payment")),
    path("paypal/", include("paypal.standard.ipn.urls")),
    path("orders/", include("orders.urls", namespace="orders")),
    path("user_wallet/", include("wallet.urls", namespace="wallet")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
