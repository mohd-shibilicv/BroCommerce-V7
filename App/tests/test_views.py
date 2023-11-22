from importlib import import_module

from django.conf import settings
from django.http import HttpRequest
from django.test import TestCase
from django.test.client import Client, RequestFactory
from django.urls import reverse

from accounts.models import Customer
from App.models import Category, Product, ProductType, ProductLanguage
from App.views import all_products


class TestViewResponse(TestCase):
    def setUp(self):
        self.client = Client()
        # self.factory = RequestFactory()
        self.category = Category.objects.create(name='django', slug='django')
        product_type = ProductType.objects.create(name='Test')
        language = ProductLanguage.objects.create(name='English')
        self.user = Customer.objects.create(username='admin')
        self.data1 = Product.objects.create(
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

    def test_url_allowed_hosts(self):
        ''' Test Allowed Hosts '''
        response = self.client.get('/shop/', HTTP_HOST='127.0.0.1')
        self.assertEqual(response.status_code, 200)

    def test_product_detail_url(self):
        ''' Test Product Page Urls'''
        response = self.client.get(reverse('App:product_details', kwargs={'slug': self.data1.slug}))
        self.assertEqual(response.status_code, 200)

    def test_category_list_url(self):
        ''' Test Category List Urls'''
        response = self.client.get(reverse('App:category_list', kwargs={'category_slug': self.category.slug}))
        self.assertEqual(response.status_code, 200)

    def test_homepage_html(self):
        request = HttpRequest()
        engine = import_module(settings.SESSION_ENGINE)
        request.session = engine.SessionStore()
        response = all_products(request)
        html = response.content.decode('utf8')
        self.assertTrue(html.startswith('\n\n<!DOCTYPE html>\n'))
        self.assertEqual(response.status_code, 200)

    # def test_view_function(self):
    #     request = self.factory.get(reverse('App:product_details', kwargs={'slug': self.data1.slug}))
    #     response = all_products(request)
    #     self.assertEqual(response.status_code, 200)

    def test_all_products_view_rendering(self):
        # Test if the view renders the correct template
        response = self.client.get(reverse('App:all_products'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'App/index.html')
