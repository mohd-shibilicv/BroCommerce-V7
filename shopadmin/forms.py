from django import forms
from django.forms import modelformset_factory

from accounts.models import Customer
from App.models import (Category, CategoryOffers, Product, ProductImage,
                        ProductOffer, ProductSpecificationValue)
from checkout.models import Coupon, DeliveryOptions
from orders.models import Order


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "parent", "is_active", "on_sale"]


class CategoryOfferForm(forms.ModelForm):
    class Meta:
        model = CategoryOffers
        fields = ["category", "valid_from", "valid_to", "discount", "is_active"]
        widgets = {
            "valid_from": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "valid_to": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }


class ProductForm(forms.ModelForm):
    cover_image = forms.ImageField(
        label="Cover image", widget=forms.FileInput(attrs={"id": "id_file"})
    )

    class Meta:
        model = Product
        fields = (
            "cover_image",
            "product_type",
            "category",
            "language",
            "author",
            "title",
            "description",
            "regular_price",
            "product_stock",
            "on_sale",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].required = True


class EditProductForm(forms.ModelForm):
    cover_image = forms.ImageField(
        label="Cover image", widget=forms.FileInput(attrs={"id": "edit_id_file"})
    )

    class Meta:
        model = Product
        fields = (
            "cover_image",
            "product_type",
            "category",
            "language",
            "author",
            "title",
            "description",
            "regular_price",
            "product_stock",
            "on_sale",
        )


class EditProductSpecificationValueForm(forms.ModelForm):
    class Meta:
        model = ProductSpecificationValue
        fields = ["specification", "value"]


ProductSpecificationValueFormSet = modelformset_factory(
    ProductSpecificationValue,
    fields=("specification", "value"),
    extra=3,
    max_num=3,
    min_num=1,
)


class EditProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = [
            "image",
            "alt_text",
            "is_feature",
            "crop_left",
            "crop_upper",
            "crop_right",
            "crop_lower",
        ]


ProductImageFormSet = modelformset_factory(
    ProductImage,
    fields=(
        "image",
        "alt_text",
        "is_feature",
        "crop_left",
        "crop_upper",
        "crop_right",
        "crop_lower",
    ),
    extra=3,
    max_num=4,
    min_num=1,
)


class ProductOfferForm(forms.ModelForm):
    class Meta:
        model = ProductOffer
        fields = ["product", "valid_from", "valid_to", "discount", "is_active"]
        widgets = {
            "valid_from": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "valid_to": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }


class AdminUserForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    is_active = forms.BooleanField(
        label="Is Active", required=True, help_text="Allow the admin to be active"
    )

    class Meta:
        model = Customer
        fields = ["email", "password", "username", "mobile", "is_active"]

    def clean_username(self):
        username = self.cleaned_data["username"].lower()
        user = Customer.objects.filter(username=username)

        if user.count():
            raise forms.ValidationError("Username already exists")

        return username

    def clean_password(self):
        pass1 = self.cleaned_data["password"]

        if len(pass1) < 8:
            raise forms.ValidationError("Password must have 8 characters")

        return pass1


class DeliveryOptionsForm(forms.ModelForm):
    class Meta:
        model = DeliveryOptions
        fields = [
            "delivery_name",
            "delivery_price",
            "delivery_method",
            "delivery_timeframe",
            "delivery_window",
            "order",
            "is_active",
        ]


class AdminOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["order_status", "delivery_status", "billing_status"]


class AddCouponForm(forms.ModelForm):
    user = forms.ModelMultipleChoiceField(
        queryset=Customer.objects.all(),
        widget=forms.SelectMultiple(
            attrs={
                "class": "w-full py-2 px-3 border rounded-md focus:outline-none focus:border-indigo-500"
            }
        ),
    )
    code = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "w-full py-2 px-3 border rounded-md focus:outline-none focus:border-indigo-500"
            }
        ),
    )

    discount = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "class": "w-full py-2 px-3 border rounded-md focus:outline-none focus:border-indigo-500"
            }
        ),
    )

    class Meta:
        model = Coupon
        fields = ["user", "code", "discount", "valid_from", "valid_to", "active"]
        widgets = {
            "valid_from": forms.DateTimeInput(
                attrs={
                    "type": "datetime-local",
                    "class": "w-full py-2 px-3 border rounded-md focus:outline-none focus:border-indigo-500",
                }
            ),
            "valid_to": forms.DateTimeInput(
                attrs={
                    "type": "datetime-local",
                    "class": "w-full py-2 px-3 border rounded-md focus:outline-none focus:border-indigo-500",
                }
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        valid_from = cleaned_data.get("valid_from")
        valid_to = cleaned_data.get("valid_to")

        if valid_from and valid_to and valid_from > valid_to:
            raise forms.ValidationError(
                "Valid from date must be less than valid to date."
            )

        return cleaned_data
