from django.test import TestCase
from django.test.client import Client
from authapp.models import ShopUser
from django.core.management import call_command

# Create your tests here.
class TestUserManagement(TestCase):
    def setUp(self):
        call_command('flush', '--noinput')
        call_command('loaddata', 'test_db.json')
        self.client = Client()

        self.superuser = ShopUser.objects.create_superuser(\
            'django2', 'django2@geekshop.local','geekshop')

        self.user = ShopUser.objects.create_user(\
            'tarantino', 'tarantion@geekshop.local', 'geekshop')

        self.user_with_first_name = ShopUser.objects.create_user(\
            'umaturman', 'umaturman@geekshop.local', 'geekshop', first_name='Uma')

    def test_user_login(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_anonymous)
        self.assertEqual(response.context['title'], 'Главная')  #?
        self.assertNotContains(response, 'User', status_code=200)
        # self.assert.NotIn('User', response.contetn.decode())
        self.client.login(username='tarantino', password='geekshop')

        response.self.client('/authapp/login/')
        self.assertFalse(response.context['user'].is_anonymous)
        self.assertEqual(response.context['user'], self.user)

        response = self.client.get('/')
        self.assertFalse(response.context['user'].is_anonymous)
        self.assertEqual(response.context['user'], self.user)
        # self.assertIn('User', response.content.decode())

    def tearDown(self):
        call_command('sqlsequencereset', 'mainapp', 'authapp', 'ordersapp', 'basketapp')

    def test_basket_login_redirect(self):
        # без логина должен переадресовать
        response = self.client.get('/basket/')
        self.assertEqual(response.url, '/auth/login/?next=/basket/')
        self.assertEqual(response.status_code, 302)
        # с логином все должно быть хорошо
        self.client.login(username='tarantino', password='geekbrains')
        response = self.client.get('/basket/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['basket']), [])
        self.assertEqual(response.request['PATH_INFO'], '/basket/')
        self.assertIn('Ваша корзина, Пользователь', response.content.decode())

def test_user_logout(self):
    # данные пользователя
    self.client.login(username='tarantino', password='geekbrains')
    # логинимся
    response = self.client.get('/auth/login/')
    self.assertEqual(response.status_code, 200)
    self.assertFalse(response.context['user'].is_anonymous)
    
    # выходим из системы
    response = self.client.get('/auth/logout/')
    self.assertEqual(response.status_code, 302)
    # главная после выхода
    response = self.client.get('/')
    self.assertEqual(response.status_code, 200)
    self.assertTrue(response.context['user'].is_anonymous)

    