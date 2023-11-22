from datetime import datetime, timedelta
from decimal import Decimal

import pyotp
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db import transaction
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from App.models import Product
from checkout.models import Coupon
from orders.forms import OrderReturnForm
from orders.models import Order
from wallet.models import Transaction, Wallet

from .forms import (PasswordChangeCustomForm, RegistrationForm,
                    UserAddressForm, UserEditForm, UserLoginForm)
from .models import Address, Customer, Referral
from .signals import user_registered
from .token import account_activation_token


class CustomLoginView(LoginView):
    form_class = UserLoginForm
    template_name = "registration/login.html"
    success_url = "/shop/"

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        return super().dispatch(request, *args, *kwargs)


def otp_login(request):
    error_message = None
    if request.method == "POST":
        email = request.POST.get("email")
        request.session["email"] = email
        try:
            user = get_object_or_404(Customer, email=email)
        except Http404:
            error_message = "Invalid Email"
            return render(
                request, "registration/otp_login.html", {"error_message": error_message}
            )

        totp = pyotp.TOTP(pyotp.random_base32(), interval=60)
        otp = totp.now()
        request.session["otp_secret_key"] = totp.secret
        valid_date = datetime.now() + timedelta(seconds=60)
        request.session["otp_valid_date"] = str(valid_date)
        print(f"Your one time password is {otp}")
        return redirect("account:verify_otp")

    return render(request, "registration/otp_login.html")


def resend_otp(request):
    if request.method == "GET":
        # Generate a new OTP and update the session data
        totp = pyotp.TOTP(pyotp.random_base32(), interval=60)
        otp = totp.now()
        request.session["otp_secret_key"] = totp.secret
        valid_date = datetime.now() + timedelta(seconds=60)
        request.session["otp_valid_date"] = str(valid_date)
        print(f"Your new one-time password is {otp}")
        return redirect("account:verify_otp")

    return render(request, "registration/verify_otp.html")


def verify_otp(request):
    error_message = None
    if request.method == "POST":
        otp = request.POST.get("otp")
        print(otp)
        email = request.session.get("email")
        otp_secret_key = request.session.get("otp_secret_key")
        otp_valid_date = request.session.get("otp_valid_date")

        if otp_secret_key and otp_valid_date is not None:
            valid_until = datetime.fromisoformat(otp_valid_date)

            if valid_until > datetime.now():
                totp = pyotp.TOTP(otp_secret_key, interval=60)
                print(totp.verify(otp))
                if totp.verify(otp):
                    user = get_object_or_404(Customer, email=email)
                    login(
                        request,
                        user,
                        backend="django.contrib.auth.backends.ModelBackend",
                    )

                    del request.session["otp_secret_key"]
                    del request.session["otp_valid_date"]

                    return redirect("account:dashboard")
                else:
                    error_message = "Invalid OTP"
            else:
                error_message = "OTP has expired"
        else:
            error_message = "Something went wrong, Try again"

    context = {"error_message": error_message}
    return render(request, "registration/verify_otp.html", context=context)


@transaction.atomic
def apply_referral_offer(reffering_user, reffered_user):
    try:
        offer_amount = Decimal(100)

        reffering_wallet = get_object_or_404(Wallet, user=reffering_user)
        reffering_wallet.balance += offer_amount
        reffering_wallet.save()

        referred_wallet = get_object_or_404(Wallet, user=reffered_user)
        referred_wallet.balance += offer_amount
        referred_wallet.save()

        Transaction.objects.create(
            user=reffering_user,
            transaction_type=Transaction.TransactionTypes.REFEREL,
            amount=offer_amount,
        )
        Transaction.objects.create(
            user=reffered_user,
            transaction_type=Transaction.TransactionTypes.REFEREL,
            amount=offer_amount,
        )
    except Exception as e:
        print(f"Error applying referral offer: {e}")
        return False


def account_register(request):
    if request.user.is_authenticated:
        return redirect("App:all_products")

    referral_code = request.GET.get("ref")
    referring_customer = None

    if referral_code:
        try:
            referring_customer = Customer.objects.get(referral_code=referral_code)
        except (Customer.DoesNotExist, ValidationError):
            messages.error(request, "Invalid or expired referral link.")
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data["email"]
            user.set_password(form.cleaned_data["password"])
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            # Send activation email
            user_registered.send(
                sender=user.__class__, user=user, current_site=current_site
            )
            user.set_activation_link_expiry()  # Set the activation link expiry
            user.save()

            Wallet.objects.create(user=user, balance=0.00)

            # Link the new user to the referring customer
            if referring_customer:
                Referral.objects.create(
                    referring_customer=referring_customer, referred_customer=user
                )
                reffering_user = get_object_or_404(Customer, pk=referring_customer.id)
                apply_referral_offer(reffering_user=reffering_user, reffered_user=user)

            messages.success(
                request,
                "Your account has been created successfully. An activation email has been sent to your email.",
            )
            return redirect("account:login")
    else:
        form = RegistrationForm()

    context = {"form": form}
    return render(request, "registration/register.html", context)


def activate_account(request):
    user = Customer.objects.all().last()
    user.is_active = True
    user.save()
    login(request, user, backend="django.contrib.auth.backends.ModelBackend")
    return redirect("account:dashboard")


def account_activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Customer.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Customer.DoesNotExist):
        user = None
    
    activation_expiry_str = user.activation_link_expiry

    if activation_expiry_str:
        activation_expiry = datetime.fromisoformat(activation_expiry_str)
        if timezone.now() > activation_expiry:
            messages.error(request, "Activation link has expired.")
            return redirect("account:login")

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user, backend="django.contrib.auth.backends.ModelBackend")
        messages.success(request, "Your account has been activated successfully.")
        return redirect("account:dashboard")
    else:
        return render(request, "registration/activation_invalid.html")


@login_required
def dashboard(request):
    user_orders = Order.objects.filter(user=request.user)[:5]
    current_site = get_current_site(request)
    return render(
        request,
        "accounts/user/dashboard.html",
        {"orders": user_orders, "current_site": current_site},
    )


@login_required
def edit_details(request):
    if request.method == "POST":
        form = UserEditForm(request.POST, request.FILES, instance=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, "Your account has been updated successfully.")
            return redirect("account:dashboard")
    else:
        form = UserEditForm(instance=request.user)

    context = {"form": form}
    return render(request, "accounts/user/edit_details.html", context)


@login_required
def delete_user(request):
    user = Customer.objects.get(username=request.user)
    user.is_active = False
    user.save()
    logout(request)

    messages.success(request, "Your account has been deleted successfully.")
    return redirect("account:login")


class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = PasswordChangeCustomForm
    template_name = "accounts/user/password_update.html"
    success_url = "/account/dashboard"

    def form_valid(self, form):
        messages.success(self.request, "Your password has been successfully changed.")
        return super().form_valid(form)


# Address
@login_required
def view_addresses(request):
    addresses = Address.objects.filter(customer=request.user)
    context = {"addresses": addresses}
    return render(request, "accounts/user/addresses.html", context)


@login_required
def add_address(request):
    if request.method == "POST":
        address_form = UserAddressForm(data=request.POST)
        if address_form.is_valid():
            address = address_form.save(commit=False)
            address.customer = request.user
            address.save()
            messages.success(request, "Address added successfully")
            return HttpResponseRedirect(reverse("account:addresses"))
    else:
        address_form = UserAddressForm()

    context = {"form": address_form}
    return render(request, "accounts/user/add_address.html", context)


@login_required
def edit_address(request, id):
    address = get_object_or_404(Address, pk=id, customer=request.user)
    if request.method == "POST":
        address_form = UserAddressForm(instance=address, data=request.POST)

        if address_form.is_valid():
            address_form.save()
            messages.success(request, "Address updated successfully")

            if "delivery_address" in request.META.get("HTTP_REFERER"):
                return HttpResponseRedirect(reverse("checkout:delivery_address"))

            return HttpResponseRedirect(reverse("account:addresses"))
    else:
        address_form = UserAddressForm(instance=address)

    context = {"form": address_form}
    return render(request, "accounts/user/edit_address.html", context)


@login_required
def delete_address(request, id):
    address = get_object_or_404(Address, pk=id, customer=request.user)
    if address.default:
        messages.error(request, "Default address can't be deleted")
        if "delivery_address" in request.META.get("HTTP_REFERER"):
            return HttpResponseRedirect(reverse("checkout:delivery_address"))
    else:
        address.delete()
        if "delivery_address" in request.META.get("HTTP_REFERER"):
            return HttpResponseRedirect(reverse("checkout:delivery_address"))
        messages.success(request, "Address deleted successfully")

    return HttpResponseRedirect(reverse("account:addresses"))


@login_required
def set_default_address(request, id):
    Address.objects.filter(customer=request.user, default=True).update(default=False)
    Address.objects.filter(pk=id, customer=request.user).update(default=True)

    if "delivery_address" in request.META.get("HTTP_REFERER"):
        return HttpResponseRedirect(reverse("checkout:delivery_address"))

    return HttpResponseRedirect(reverse("account:addresses"))


# Wishlist
@login_required
def user_wishlist(request):
    products = Product.objects.filter(user_wishlist=request.user)

    context = {"wishlist": products}
    return render(request, "accounts/user/user_wishlist.html", context)


@login_required
def add_to_wishlist(request, id):
    product = get_object_or_404(Product, id=id)
    if product.user_wishlist.filter(id=request.user.id).exists():
        product.user_wishlist.remove(request.user)
        messages.success(request, "Removed from wishlist successfully")
    else:
        product.user_wishlist.add(request.user)
        messages.success(request, "Added to wishlist successfully")

    return HttpResponseRedirect(request.META["HTTP_REFERER"])


# Orders
@login_required
def user_orders(request):
    user_id = request.user.id
    orders = Order.objects.filter(user_id=user_id)

    sort_param = request.GET.get("sort")

    if sort_param == "default":
        orders = orders.order_by("-created")
    elif sort_param == "paid":
        orders = orders.filter(order_status=Order.OrderStatus.PAID).order_by("-created")
    elif sort_param == "pending":
        orders = orders.filter(order_status=Order.OrderStatus.PENDING).order_by(
            "-created"
        )
    elif sort_param == "cancelled":
        orders = orders.filter(order_status=Order.OrderStatus.CANCELLED).order_by(
            "-created"
        )

    orders_per_page = 10
    paginator = Paginator(orders, orders_per_page)
    page_number = request.GET.get("page")
    orders_on_page = paginator.get_page(page_number)

    context = {"orders": orders_on_page, "sort_param": sort_param}
    return render(request, "accounts/user/orders.html", context)


@login_required
def view_order_details(request, id):
    order = get_object_or_404(Order, pk=id)

    current_date = timezone.now()
    ordered_date = order.created

    days_difference = (current_date - ordered_date).days

    if request.method == "POST":
        if days_difference <= 10:
            form = OrderReturnForm(request.POST, request.FILES)
            if form.is_valid():
                return_form = form.save(commit=False)
                return_form.user = order.user
                return_form.order = order
                return_form.save()

                order.order_status = order.OrderStatus.REQUESTED
                order.save()

                messages.success(request, "Order return request sent")
                return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
            else:
                print(form.errors)
        else:
            messages.info(
                request,
                "Order return is not allowed for orders placed more than 10 days ago.",
            )
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    else:
        form = OrderReturnForm()

    context = {"order": order, "form": form}
    return render(request, "accounts/user/view_order_details.html", context)


@login_required
def cancel_order(request, id):
    order = get_object_or_404(Order, pk=id)
    if order.order_status == Order.OrderStatus.PENDING:
        for item in order.items.all():
            product = item.product
            product.product_stock += item.quantity
            product.save()

        order.order_status = Order.OrderStatus.CANCELLED
        order.delivery_status = Order.DeliveryStatus.REJECTED
        order.save()
        messages.info(request, "Order Cancelled!")

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required
def delete_order(request, id):
    order = get_object_or_404(Order, pk=id)
    order.delete()
    messages.success(request, "Order deleted successfully")
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required
def user_profile(request):
    user = request.user
    return render(request, "accounts/user/user_profile.html", {"user": user})


@login_required
def user_coupons(request):
    coupons = Coupon.objects.filter(
        user=request.user,
    )
    return render(request, 'accounts/user/user_coupons.html', {'coupons': coupons})


@login_required
def remove_user_coupon(request, coupon_id):
    coupon = get_object_or_404(Coupon, pk=coupon_id)

    if request.user in coupon.user.all():
        coupon.user.remove(request.user)
        messages.success(request, f'Coupon \'{coupon.code}\' removed')
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    else:
        messages.error(request, 'You don\'t have the permission to remove this coupon')
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
