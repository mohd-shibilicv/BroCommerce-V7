from django import forms
from django.utils.translation import gettext_lazy as _


class WalletForm(forms.Form):
    amount = forms.DecimalField(
        label=_("Amount"),
        max_digits=10,
        decimal_places=2,
        min_value=0.01,
    )

    def clean_amount(self):
        amount = self.cleaned_data["amount"]
        if amount <= 0:
            raise forms.ValidationError(_("Amount must be greater than 0"))
        return amount
