import debug_toolbar
import environ
import os

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, 'brocommerce/settings/.env'))

urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("accounts/", include("allauth.urls")),
    path(env("SECRET_ADMIN_URL") + "/admin/", admin.site.urls),
    path("shopadmin/", include("shopadmin.urls", namespace="shopadmin")),
    path("__debug__/", include(debug_toolbar.urls)),
    path("", include("home.urls", namespace="home")),
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
