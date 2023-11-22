from django import forms
from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .models import (Category, CategoryOffers, Product, ProductImage,
                     ProductLanguage, ProductOffer, ProductSpecification,
                     ProductSpecificationValue, ProductType)


@admin.register(CategoryOffers)
class CategoryOffersAdmin(admin.ModelAdmin):
    list_display = ["category", "discount", "is_active"]
    list_editable = ["is_active"]


@admin.register(ProductOffer)
class ProductOfferAdmin(admin.ModelAdmin):
    list_display = ["product", "discount", "is_active"]
    list_editable = ["is_active"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    model = MPTTModelAdmin
    list_display = ["name", "is_active"]
    list_editable = ["is_active"]
    prepopulated_fields = {"slug": ("name",)}


class ProductSpecificationInline(admin.TabularInline):
    model = ProductSpecification


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    inlines = [
        ProductSpecificationInline,
    ]


class ProductImageInline(admin.TabularInline):
    model = ProductImage


class ProductSpecificationValueInline(admin.TabularInline):
    model = ProductSpecificationValue


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ProductSpecificationValueInline,
        ProductImageInline,
    ]
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(ProductLanguage)
