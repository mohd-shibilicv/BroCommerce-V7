from django import forms


class CouponForm(forms.Form):
    code = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter your coupon code",
                "id": "coupon_input",
                "onfocus": "fetchCoupons()",
            }
        )
    )
