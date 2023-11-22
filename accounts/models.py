import uuid

from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models
from django.shortcuts import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class CustomAccountManager(BaseUserManager):
    def create_superuser(self, email, username, password, **other_fields):
        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)
        other_fields.setdefault("is_active", True)

        if other_fields.get("is_staff") is not True:
            raise ValueError("Superuser must be a staff.")
        if other_fields.get("is_superuser") is not True:
            raise ValueError("You're not a superuser.")

        return self.create_user(email, username, password, **other_fields)

    def create_user(self, email, username, password, **other_fields):
        if not email:
            raise ValueError(_("You should provide an email address."))

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **other_fields)
        user.set_password(password)
        user.save()
        return user


# class UserBase(AbstractBaseUser, PermissionsMixin):
#     email = models.EmailField(_('email address'), unique=True)
#     username = models.CharField(max_length=150, unique=True)
#     first_name = models.CharField(max_length=150, unique=False)
#     about = models.TextField(_('about'), max_length=500, blank=True)

#     # Delivery Details
#     country = CountryField()
#     phone_number = models.CharField(max_length=15, blank=True)
#     postcode = models.CharField(max_length=12, blank=True)
#     address_line1 = models.CharField(max_length=150, blank=True)
#     address_line2 = models.CharField(max_length=150, blank=True)
#     town_city = models.CharField(max_length=150, blank=True)

#     # User Status
#     profile = models.ImageField(upload_to='users/', default='users/default_user.png')
#     is_active = models.BooleanField(default=False)
#     is_staff = models.BooleanField(default=False)
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)

#     # Custom Manager
#     objects = CustomAccountManager()

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username']

#     class Meta:
#         verbose_name = 'Account'
#         verbose_name_plural = 'Accounts'

#     def __str__(self):
#         return self.username


class Customer(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    username = models.CharField(max_length=150)
    mobile = models.CharField(max_length=20, blank=True)

    # User Status
    profile = models.ImageField(upload_to="users/", default="users/default_user.png")
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    activation_link_expiry = models.CharField(max_length=50, null=True, blank=True)

    # Referral
    referral_code = models.UUIDField(default=uuid.uuid4, editable=False, unique=False)
    referral_link = models.URLField(blank=True)

    # Custom Manager
    objects = CustomAccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = "Account"
        verbose_name_plural = "Accounts"

    def __str__(self):
        return self.username

    def set_activation_link_expiry(self):
        expiry_time = timezone.now() + timezone.timedelta(hours=24)
        self.activation_link_expiry = expiry_time.isoformat()

    def save(self, *args, **kwargs):
        if not self.referral_link:
            self.referral_link = (
                reverse("account:register") + f"?ref={str(self.referral_code)}"
            )
        super().save(*args, **kwargs)


class Referral(models.Model):
    referring_customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="referrals",
        null=True,
        blank=True,
    )
    referred_customer = models.OneToOneField(
        Customer,
        on_delete=models.CASCADE,
        related_name="referred_by",
        null=True,
        blank=True,
    )
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"{self.referring_customer.username} -> {self.referred_customer.username}"
        )


class Address(models.Model):
    """
    Address Model
    """

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    customer = models.ForeignKey(
        Customer,
        verbose_name=_("Customer"),
        related_name="customer_address",
        on_delete=models.CASCADE,
    )
    full_name = models.CharField(_("Full Name"), max_length=150)
    email = models.EmailField(max_length=255, blank=True)
    phone = models.CharField(_("Phone Number"), max_length=20)
    postcode = models.CharField(_("Postcode"), max_length=50)
    address_line = models.CharField(_("Address Line 1"), max_length=255)
    address_line2 = models.CharField(_("Address Line 2"), max_length=255)
    town_city = models.CharField(_("Town/City/State"), max_length=150)
    delivery_instructions = models.CharField(_("Delivery Instructions"), max_length=255)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
    default = models.BooleanField(_("Default"), default=False)

    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"

    def __str__(self):
        return f"{self.full_name} Address"
