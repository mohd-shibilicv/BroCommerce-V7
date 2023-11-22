from django.contrib.auth.models import User
from django.test import TestCase

from App.models import Category, Product


class TestCategoriesModel (TestCase):

    def setUp(self):
        self.data1 = Category.objects.create(name='django', slug='django')

    def test_category_model_entry(self):
        """
        Test Category model data insertion/types/field attributes
        """
        self.assertIsInstance(self.data1, Category)

    def test_category_model_default_name(self):
        """
        Test Category model dafault name
        """
        default_name = str(self.data1)
        self.assertEqual(default_name, 'django')


class TestProductsModel(TestCase):

    def setUp(self):
        category = Category.objects.create(name='django', slug='django')
        user = User.objects.create(username='admin')
        self.data1 = Product.objects.create(
            title='Django Tutorial 1',
            author=user.username,
            description='New description',
            image='images/django-project-min.png',
            slug='django-tutorial-1', price='29.99',
            in_stock=True,
            is_active=True,
            created_by_id=1,
            category_id=category.id
        )

    def test_product_model_entry(self):
        '''
        Test Product model entry attributes
        '''
        data = self.data1
        self.assertTrue(isinstance(data, Product))
        self.assertEqual(str(data), data.title)
