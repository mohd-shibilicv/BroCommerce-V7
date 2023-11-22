from django.urls import path

from . import views

app_name = "wallet"

urlpatterns = [
    path("", views.user_wallet, name="user_wallet"),
    path("deposit/", views.deposit_view, name="deposit_view"),
    path("withdraw/", views.withdraw_view, name="withdraw_view"),
    path(
        "clear_transactions_history/",
        views.clear_transactions_history,
        name="clear_transactions_history",
    ),
]
