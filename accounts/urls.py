from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = "account"

urlpatterns = [
    path("register", views.account_register, name="register"),
    path("login", views.CustomLoginView.as_view(), name="login"),
    path("otp_login", views.otp_login, name="otp_login"),
    path("verify_otp", views.verify_otp, name="verify_otp"),
    path("resend-otp/", views.resend_otp, name="resend_otp"),
    path("logout", auth_views.LogoutView.as_view(), name="logout"),
    path(
        "reset-password/", auth_views.PasswordResetView.as_view(), name="reset-password"
    ),
    path(
        "password-reset-done/",
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "password-change/",
        views.CustomPasswordChangeView.as_view(),
        name="password_change",
    ),
    path(
        "password-change-done/",
        auth_views.PasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
    path("activate_account/", views.activate_account, name="activate_account"),
    path(
        "activate/<slug:uidb64>/<slug:token>/", views.account_activate, name="activate"
    ),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("profile/", views.user_profile, name="user_profile"),
    path("profile/edit/", views.edit_details, name="edit_details"),
    path("profile/delete_user/", views.delete_user, name="delete_user"),
    # Address URLs
    path("addresses/", views.view_addresses, name="addresses"),
    path("add_address/", views.add_address, name="add_address"),
    path("addresses/edit/<uuid:id>/", views.edit_address, name="edit_address"),
    path("addresses/delete/<uuid:id>/", views.delete_address, name="delete_address"),
    path(
        "addresses/set_default/<uuid:id>/",
        views.set_default_address,
        name="set_default_address",
    ),
    # Wishlist URLs
    path("user_wishlist/", views.user_wishlist, name="user_wishlist"),
    path("wishlist/add/<int:id>/", views.add_to_wishlist, name="add_to_wishlist"),
    # Order URLs
    path("orders/", views.user_orders, name="user_orders"),
    path(
        "view_order_details/<int:id>/",
        views.view_order_details,
        name="view_order_details",
    ),
    path("cancel_order/<int:id>/", views.cancel_order, name="cancel_order"),
    path("delete_order/<int:id>/", views.delete_order, name="delete_order"),
    # Coupon URLs
    path('coupons/', views.user_coupons, name='coupons'),
    path('remove_coupon/<int:coupon_id>/', views.remove_user_coupon, name='remove_coupon'),
]
