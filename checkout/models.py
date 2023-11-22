from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from accounts.models import Customer


class DeliveryOptions(models.Model):
    """
    Contains all delivery methods
    """

    DELIVERY_CHICES = [
        ("IS", "In Store"),
        ("HD", "Home Delivery"),
        ("DD", "Digital Delivery"),
    ]

    delivery_name = models.CharField(
        verbose_name=_("Delivery Name"), help_text=_("Required"), max_length=255
    )
    delivery_price = models.DecimalField(
        verbose_name=_("Delivery Price"),
        help_text=_("Maximum 999.99"),
        error_messages={
            "name": {
                "max_length": _("The price must be between 0 and 999.99"),
            }
        },
        max_digits=5,
        decimal_places=2,
    )
    delivery_method = models.CharField(
        choices=DELIVERY_CHICES,
        verbose_name=_("Delivery Method"),
        help_text=_("Required"),
        max_length=255,
    )
    delivery_timeframe = models.CharField(
        verbose_name=_("Delivery Timeframe"), help_text=_("Required"), max_length=255
    )
    delivery_window = models.CharField(
        verbose_name=_("Delivery Window"), help_text=_("Required"), max_length=255
    )
    order = models.IntegerField(
        verbose_name=_("List Order"), help_text=_("Required"), default=0
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Delivery Option")
        verbose_name_plural = _("Delivery Options")
        ordering = ("order",)

    def __str__(self):
        return self.delivery_name


class PaymentSelections(models.Model):
    """
    Contains payment options
    """

    name = models.CharField(
        verbose_name=_("Name"), help_text=_("Required"), max_length=255
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Payment Selection")
        verbose_name_plural = _("Payment Selections")

    def __str__(self):
        return self.name


class Coupon(models.Model):
    user = models.ManyToManyField(Customer, related_name="coupons", blank=True)
    code = models.CharField(max_length=50, unique=True)
    discount = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)], default=0
    )
    active = models.BooleanField(default=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()

    def __str__(self):
        return self.code

    def is_expired(self):
        return self.valid_to < timezone.now()

    def save(self, *args, **kwargs):
        if self.is_expired() and self.active:
            self.active = False
        super().save(*args, **kwargs)
