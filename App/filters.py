import django_filters
from django import forms

from App.models import Category, Product, ProductLanguage


class ProductFilter(django_filters.FilterSet):
    regular_price = django_filters.RangeFilter(label="Price between")
    created_at = django_filters.DateRangeFilter(label="Released on")

    class Meta:
        model = Product
        fields = {
            "product_type": ["exact"],
            "category": ["exact"],
            "language": ["exact"],
        }
