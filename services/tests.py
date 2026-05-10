from django.test import TestCase, Client
from .models import Service


class ServiceModelTest(TestCase):
    """Тесты модели Service"""

    def setUp(self):
        # setUp — запускается перед каждым тестом
        # Создаём тестовую услугу
        self.service = Service.objects.create(
            name='Оздоровительный массаж',
            service_type='classic',
            description='Расслабляющий массаж',
            price=2000,
            duration=60,
            is_active=True
        )

    def test_service_created(self):
        """Услуга создаётся корректно"""
        self.assertEqual(self.service.name, 'Оздоровительный массаж')
        self.assertEqual(self.service.price, 2000)

    def test_service_str(self):
        """Метод __str__ возвращает правильную строку"""
        expected = 'Оздоровительный массаж — 2000 руб.'
        self.assertEqual(str(self.service), expected)

    def test_inactive_service(self):
        """Неактивная услуга не отображается"""
        self.service.is_active = False
        self.service.save()
        active = Service.objects.filter(is_active=True)
        self.assertEqual(active.count(), 0)


class ServiceViewTest(TestCase):
    """Тесты страниц"""

    def setUp(self):
        self.client = Client()
        self.service = Service.objects.create(
            name='Релакс  массаж',
            service_type='relax',
            description='Массаж горячими камнями',
            price=3000,
            duration=90,
            is_active=True
        )

    def test_home_page(self):
        """Главная страница открывается"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_service_list_page(self):
        """Страница услуг открывается"""
        response = self.client.get('/services/')
        self.assertEqual(response.status_code, 200)

    def test_service_in_list(self):
        """Услуга отображается на странице"""
        response = self.client.get('/services/')
        self.assertContains(response, 'Релакс  массаж')

    def test_inactive_service_not_in_list(self):
        """Неактивная услуга не показывается на сайте"""
        self.service.is_active = False
        self.service.save()
        response = self.client.get('/services/')
        self.assertNotContains(response, 'Релакс  массаж')