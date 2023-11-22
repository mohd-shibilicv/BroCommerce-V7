from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from App.models import Category, Product, ProductType, ProductLanguage
from accounts.models import Customer


class TestCartView(TestCase):
    def setUp(self):
        self.user = Customer.objects.create(username="admin")
        self.category = Category.objects.create(name="django", slug="django")
        product_type = ProductType.objects.create(name='Test')
        language = ProductLanguage.objects.create(name='English')
        Product.objects.create(
            title='Django Tutorial 1',
            author=self.user.username,
            description='New description',
            cover_image='images/the_art_of_war.jpg',
            slug='django-tutorial-1',
            regular_price='29.99',
            product_stock=100,
            is_active=True,
            category_id=self.category.id,
            product_type=product_type,
            language=language,
        )
        Product.objects.create(
            title='Django Tutorial 2',
            author=self.user.username,
            description='New description',
            cover_image='images/the_art_of_war.jpg',
            slug='django-tutorial-2',
            regular_price='29.99',
            product_stock=100,
            is_active=True,
            category_id=self.category.id,
            product_type=product_type,
            language=language,
        )
        Product.objects.create(
            title='Django Tutorial 3',
            author=self.user.username,
            description='New description',
            cover_image='images/the_art_of_war.jpg',
            slug='django-tutorial-3',
            regular_price='29.99',
            product_stock=100,
            is_active=True,
            category_id=self.category.id,
            product_type=product_type,
            language=language,
        )
        self.client.post(
            reverse("cart:add_to_cart"),
            {"productid": 1, "productquantity": 1, "action": "post"},
            xhr=True,
        )
        self.client.post(
            reverse("cart:add_to_cart"),
            {"productid": 2, "productquantity": 2, "action": "post"},
            xhr=True,
        )

    def get_cart_url(self):
        """
        Test Cart Response Status
        """
        response = self.client.get(reverse("cart:view_cart"))
        self.assertEqual(response.status_code, 200)

    def test_add_to_cart(self):
        """
        Test Add to Cart functionality
        """
        response = self.client.post(
            reverse("cart:add_to_cart"),
            {"productid": 3, "productquantity": 1, "action": "post"},
            xhr=True,
        )
        self.assertEqual(response.json(), {"quantity": 4})
        response = self.client.post(
            reverse("cart:add_to_cart"),
            {"productid": 2, "productquantity": 1, "action": "post"},
            xhr=True,
        )
        self.assertEqual(response.json(), {"quantity": 3})

    def test_cart_delete(self):
        """
        Test Deleting Cart Items
        """
        response = self.client.post(
            reverse("cart:cart_delete"), {"productid": 2, "action": "post"}, xhr=True
        )
        self.assertEqual(response.json(), {"quantity": 0, "subtotal": "0"})

    def test_cart_update(self):
        """
        Test Updating Cart Items
        """
        response = self.client.post(
            reverse("cart:cart_update"),
            {"productid": 3, "productquantity": 3, "action": "post"},
            xhr=True,
        )
        self.assertEqual(response.json(), {'productquantity': 3, 'quantity': 0, 'subtotal': '0', 'total': '0'})
