from decimal import Decimal

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey
from PIL import Image


class Category(MPTTModel):
    """
    Category Table Implemented with MPTT
    """

    name = models.CharField(
        verbose_name=_("Category Name"),
        help_text=_("Required and unique"),
        max_length=255,
        unique=True,
    )
    slug = models.SlugField(
        verbose_name=_("Category safe URL"), max_length=255, unique=True
    )
    parent = TreeForeignKey(
        "self", on_delete=models.CASCADE, related_name="children", blank=True, null=True
    )
    is_active = models.BooleanField(default=True)
    on_sale = models.BooleanField(default=False)

    class MPTTMeta:
        order_insertion_by = ["name"]

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def get_absolute_url(self):
        return reverse("App:category_list", kwargs={"category_slug": self.slug})

    def __str__(self):
        return self.name


class CategoryOffers(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="category_offer"
    )
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(
        help_text=_("In Percentage"),
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        default=0,
    )
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Category Offer")
        verbose_name_plural = _("Category Offers")

    def save(self, *args, **kwargs):
        super(CategoryOffers, self).save(*args, **kwargs)
        category = get_object_or_404(Category, slug=self.category.slug)

        if self.is_active and category.on_sale:
            if category.on_sale:
                products = Product.objects.filter(category__slug=category.slug)

                for product in products:
                    new_product_discount_price = product.regular_price * (
                        1 - Decimal(self.discount) / 100
                    )
                    if product.discount_price != new_product_discount_price:
                        product.discount_price = new_product_discount_price
                        product.save()

        if not self.is_active or not self.category.on_sale or (self.valid_to and timezone.now() > self.valid_to):
            products = Product.objects.filter(category=self.category)
            for product in products:
                if not product.on_sale:
                    product.discount_price = Decimal(0)
                    product.save()


@receiver(pre_save, sender=Category)
def generate_category_slug(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)


class ProductType(models.Model):
    """
    Different Types of products
    """

    name = models.CharField(
        verbose_name=_("Product type"),
        help_text=_("Required"),
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Product Type")
        verbose_name_plural = _("Product Types")

    def __str__(self):
        return self.name


class ProductLanguage(models.Model):
    name = models.CharField(
        max_length=100, verbose_name=_("Language name"), unique=True
    )

    def __str__(self):
        return self.name


class ProductSpecification(models.Model):
    """
    Contains product specifications or features for the product types
    """

    product_type = models.ForeignKey(ProductType, on_delete=models.RESTRICT)
    name = models.CharField(
        verbose_name=_("Name"), help_text=_("Required"), max_length=255
    )

    class Meta:
        verbose_name = _("Product Specification")
        verbose_name_plural = _("Product Specifications")

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    Contains all product items
    """

    product_type = models.ForeignKey(ProductType, on_delete=models.RESTRICT)
    category = models.ForeignKey(
        Category, on_delete=models.RESTRICT, related_name="product_category"
    )
    language = models.ForeignKey(
        ProductLanguage, on_delete=models.CASCADE, null=True, blank=True
    )
    author = models.CharField(max_length=255, default="Admin")
    title = models.CharField(
        verbose_name=_("title"), help_text=_("Required"), max_length=255
    )
    description = models.TextField(
        verbose_name=_("description"), help_text=_("Optional"), blank=True
    )
    slug = models.SlugField(max_length=255)
    cover_image = models.ImageField(
        upload_to="images/", default="images/the_art_of_war.jpg"
    )
    regular_price = models.DecimalField(
        verbose_name=_("Regular Price"),
        help_text=_("Maximum 999.99"),
        error_messages={
            "name": {"max_length": _("The price must be between 0 and 999.99")}
        },
        max_digits=10,
        decimal_places=2,
    )
    discount_price = models.DecimalField(
        verbose_name=_("Discount Price"),
        max_digits=10,
        decimal_places=2,
        default=Decimal(0),
        editable=False,
    )
    is_active = models.BooleanField(
        verbose_name=_("Product visibility"),
        help_text=_("Change Product Visibility"),
        default=True,
    )
    product_stock = models.PositiveIntegerField(
        verbose_name=_("Product Stock"),
        help_text=_("Change Product Stock"),
        default=100,
    )
    created_at = models.DateTimeField(
        _("Created at"), auto_now_add=True, editable=False
    )
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
    user_wishlist = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="user_wishlist", blank=True
    )
    on_sale = models.BooleanField(default=False)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def get_absolute_url(self):
        return reverse("App:product_details", kwargs={"slug": self.slug})

    def get_images(self):
        return self.product_image.all()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super(Product, self).save(*args, **kwargs)

        product = get_object_or_404(Product, slug=self.slug)

        if not self.is_active:
            if product.on_sale:
                product.discount_price = Decimal(0)
                product.save()


class ProductOffer(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_offer')
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(
        help_text=_("In Percentage"),
        validators=[MinValueValidator(1), MaxValueValidator(100)],
    )
    is_active = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super(ProductOffer, self).save(*args, **kwargs)
        product = get_object_or_404(Product, slug=self.product.slug)
        if product.on_sale:
            if self.discount:
                new_discount_price = product.regular_price * (
                    1 - Decimal(self.discount) / 100
                )
                if product.discount_price != new_discount_price:
                    product.discount_price = new_discount_price
                    product.save()

        if not self.is_active or (self.valid_to and timezone.now() > self.valid_to):
            if product.on_sale or product.category.on_sale:
                product.discount_price = Decimal(0)
                product.save()


@receiver(pre_save, sender=Product)
def generate_product_slug(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)


class ProductSpecificationValue(models.Model):
    """
    Contains Each individual product specifications or features
    """

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    specification = models.ForeignKey(ProductSpecification, on_delete=models.RESTRICT)
    value = models.CharField(
        verbose_name=_("Value"),
        help_text=_("Product specification value"),
        max_length=255,
    )

    class Meta:
        verbose_name = _("Product Specification Value")
        verbose_name_plural = _("Product Specification Values")

    def __str__(self):
        return self.value


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, related_name="product_image", on_delete=models.CASCADE
    )
    image = models.ImageField(
        verbose_name=_("image"),
        help_text=_("Upload a product"),
        upload_to="images/",
        default="images/the_art_of_war.jpg",
    )
    alt_text = models.CharField(
        verbose_name=_("Alternative text"),
        help_text=_("Please add alternative text"),
        max_length=255,
        null=True,
        blank=True,
    )
    crop_left = models.FloatField(help_text=_('Left coordinate'), null=True, blank=True, default=0)
    crop_right = models.FloatField(help_text=_('Right coordinate'), null=True, blank=True, default=0)
    crop_upper = models.FloatField(help_text=_('Upper coordinate'), null=True, blank=True, default=0)
    crop_lower = models.FloatField(help_text=_('Lower coordinate'), null=True, blank=True, default=0)
    is_feature = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Product Image")
        verbose_name_plural = _("Product Images")


class ProductReview(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="reviews"
    )
    reviewer_name = models.CharField(_("Name"), max_length=255, default="user")
    review_profile = models.ImageField(
        upload_to="images/", default="images/default_user.png"
    )
    reviewer_email = models.EmailField(_("Email"), max_length=255, blank=True)
    review_text = models.TextField(_("Review"))
    like_count = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    purchase_verified = models.BooleanField(default=False)

    class Meta:
        ordering = ("-created",)
        verbose_name = _("Product Review")
        verbose_name_plural = _("Product Reviews")

    def __str__(self):
        return f"Review for {self.product.title} by {self.reviewer_name}"
