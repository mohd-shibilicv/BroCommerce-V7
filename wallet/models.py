from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from accounts.models import Customer


class Wallet(models.Model):
    user = models.ForeignKey(Customer, related_name="wallet", on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Wallet of {self.user.username}"


class Transaction(models.Model):
    class TransactionTypes(models.TextChoices):
        DEPOSIT = "Deposit", "Deposit"
        WITHDRAW = "Withdraw", "Withdraw"
        PURCHASE = "Purchase", "Purchase"
        RETURN = "Return", "Return"
        REFERRAL = "Referral", "Referral"

    user = models.ForeignKey(
        Customer, related_name="transactions", on_delete=models.CASCADE
    )
    transaction_type = models.CharField(max_length=10, choices=TransactionTypes.choices)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ("-timestamp",)
        verbose_name = _("Transaction")
        verbose_name_plural = _("Transactions")

    def __str__(self):
        return f"{self.transaction_type} of {self.amount} by {self.user.username}"
