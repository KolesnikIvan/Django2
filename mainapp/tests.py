from unicodedata import name
from random import randint
from django.test import TestCase, Client
from mainapp.models import ProductCategory, Product
import factory

class ProductCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductCategory

    name = factory.Sequence(lambda n: f'Ctg_{n}')


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product
    
    category = factory.SubFactory(ProductCategory)
    name = factory.Sequence(lambda n: f'Prod_{n}')
    price = randint(3,30)
    color = 0x000000
    image = factory.django.ImageField()


# Create your tests here.
class MainAppSmokeTest(TestCase):

    def setUp(self):
        # categories = ProductCategoryFactory.create_batch(10)
        categories = ProductCategoryFactory.create_batch(3)
        for cat in categories:
            ProductFactory.create_batch(10, category=cat)
        empty_category = ProductCategoryFactory.create()
        return super().setUp()

    def tearDown(self):
        return super().tearDown()

    def test_site_urls(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/contact/')
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 200)
        
        # response = self.client.get(f'/products/{category.pk}/0/')
        # self.assertEqual(response.status_code, 200)
        
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)
        
        for category in ProductCategory.objects.all():
            response = self.client.get(f'/products/category/{category.pk}')
            self.assertEqual(response.status_code, 200)

        # for product in Product.objects.all():
        #     response = self.client.get(f'/products/product/{product.pk}')
        #     self.assertEqual(response.status_code, 200)
