from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from App.models import Category, Product


class TestCartView(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="admin")
        self.category = Category.objects.create(name="django", slug="django")
        Product.objects.create(
            title="Django Tutorial 100",
            author=self.user.username,
            description="Neo description",
            image="images/django-project-min.png",
            slug="django-tutorial-1",
            price="29.99",
            in_stock=True,
            is_active=True,
            created_by_id=1,
            category_id=self.category.id,
        )
        Product.objects.create(
            title="Django Tutorial 100",
            author=self.user.username,
            description="Neo description",
            image="images/django-project-min.png",
            slug="django-tutorial-1",
            price="29.99",
            in_stock=True,
            is_active=True,
            created_by_id=1,
            category_id=self.category.id,
        )
        Product.objects.create(
            title="Django Tutorial 100",
            author=self.user.username,
            description="Neo description",
            image="images/django-project-min.png",
            slug="django-tutorial-1",
            price="29.99",
            in_stock=True,
            is_active=True,
            created_by_id=1,
            category_id=self.category.id,
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
        self.assertEqual(response.json(), {"quantity": 1, "subtotal": "29.99"})

    def test_cart_update(self):
        """
        Test Updating Cart Items
        """
        response = self.client.post(
            reverse("cart:cart_update"),
            {"productid": 2, "productquantity": 1, "action": "post"},
            xhr=True,
        )
        self.assertEqual(response.json(), {"quantity": 2, "subtotal": "59.98"})
