from decimal import Decimal

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from accounts.models import Customer
from App.models import Product
from checkout.models import Coupon


class Order(models.Model):
    class OrderStatus(models.TextChoices):
        PAID = "Paid", "Paid"
        PENDING = "Pending", "Pending"
        CANCELLED = "Cancelled", "Cancelled"
        REQUESTED = "Requested", "Requested"
        RETURNED = "Returned", "Returned"

    class DeliveryStatus(models.TextChoices):
        PROCESSING = "Processing", "Processing"
        SHIPPED = "Shipped", "Shipped"
        DELIVERED = "Delivered", "Delivered"
        COMPLETED = "Completed", "Completed"
        REJECTED = "Rejected", "Rejected"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders"
    )
    coupon = models.ForeignKey(
        Coupon,
        on_delete=models.SET_NULL,
        related_name="order_coupon",
        null=True,
        blank=True,
    )
    discount = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    full_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=255, blank=True)
    address1 = models.CharField(max_length=250)
    address2 = models.CharField(max_length=250)
    city = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    postal_code = models.CharField(max_length=20)
    country_code = models.CharField(max_length=4, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    delivery_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal(0)
    )
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal(0))
    total_paid = models.DecimalField(max_digits=10, decimal_places=2)
    order_key = models.CharField(max_length=200, unique=True)
    payment_option = models.CharField(max_length=255, blank=True)
    billing_status = models.BooleanField(default=False)
    order_status = models.CharField(
        choices=OrderStatus.choices, max_length=255, default="Pending"
    )
    delivery_status = models.CharField(
        choices=DeliveryStatus.choices, max_length=255, default="Processing"
    )

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return str(self.created)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name="order_items", on_delete=models.CASCADE
    )
    price = models.DecimalField(max_digits=5, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def get_total_price(self):
        return float(self.price * self.quantity)

    def __str__(self):
        return str(self.id)


class OrderReturn(models.Model):
    user = models.ForeignKey(
        Customer, related_name="returned_orders", on_delete=models.CASCADE
    )
    order = models.ForeignKey(
        Order, related_name="returned_order", on_delete=models.CASCADE
    )
    screenshot = models.ImageField(upload_to="images/return_screenshots/", blank=True)
    reason = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.order.order_key} returned by {self.user.username}"


class Invoice(models.Model):
    invoice_number = models.CharField(max_length=10, unique=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    issued_date = models.DateField()
    due_date = models.DateField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    items = models.ManyToManyField(OrderItem, related_name="invoice_items")

    def __str__(self):
        return self.invoice_number
