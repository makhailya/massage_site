from django.test import TestCase, Client
from django.contrib.auth.models import User
from services.models import Service
from .models import Booking


class BookingModelTest(TestCase):
    """Тесты модели Booking"""

    def setUp(self):
        # Создаём пользователя и услугу для тестов
        self.user = User.objects.create_user(
            username='testclient',
            password='testpass123'
        )
        self.service = Service.objects.create(
            name='Оздоровительный массаж',
            service_type='classic',
            description='Тест',
            price=2000,
            duration=60,
            is_active=True
        )
        self.booking = Booking.objects.create(
            client=self.user,
            service=self.service,
            date='2026-06-01',
            time='14:00',
            status='pending'
        )

    def test_booking_created(self):
        """Запись создаётся корректно"""
        self.assertEqual(self.booking.status, 'pending')
        self.assertEqual(self.booking.client.username, 'testclient')

    def test_booking_str(self):
        """Метод __str__ работает"""
        result = str(self.booking)
        self.assertIn('testclient', result)
        self.assertIn('Оздоровительный массаж', result)

    def test_booking_default_status(self):
        """Статус по умолчанию — pending"""
        self.assertEqual(self.booking.status, 'pending')


class BookingViewTest(TestCase):
    """Тесты страниц записи"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testclient',
            password='testpass123'
        )
        self.service = Service.objects.create(
            name='Релакс  массаж',
            service_type='relax',
            description='Тест',
            price=3000,
            duration=90,
            is_active=True
        )

    def test_booking_page_for_guest(self):
        """Незалогиненный видит предложение войти"""
        response = self.client.get('/booking/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'войти')

    def test_account_page_requires_login(self):
        """Личный кабинет без входа — редирект"""
        response = self.client.get('/account/')
        self.assertEqual(response.status_code, 302)  # 302 = редирект

    def test_account_page_for_logged_user(self):
        """Залогиненный видит личный кабинет"""
        self.client.login(username='testclient', password='testpass123')
        response = self.client.get('/account/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testclient')

    def test_booking_create_post(self):
        """Создание записи через форму"""
        self.client.login(username='testclient', password='testpass123')
        response = self.client.post('/booking/', {
            'service': self.service.pk,
            'date': '2026-06-15',
            'time': '15:00',
            'comment': 'Тестовая запись'
        })
        # После успешной отправки — редирект на страницу успеха
        self.assertEqual(response.status_code, 302)
        # Запись реально создалась в базе
        self.assertEqual(Booking.objects.count(), 1)
