from django.contrib.auth.models import User
from django.db import models

from services.models import Service


class Booking(models.Model):
    STATUS_CHOICES = [
        ("pending", "Ожидает подтверждения"),
        ("confirmed", "Подтверждено"),
        ("cancelled", "Отменено"),
    ]

    client = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Клиент")
    service = models.ForeignKey(
        Service, on_delete=models.CASCADE, verbose_name="Услуга"
    )
    date = models.DateField(verbose_name="Дата")
    time = models.TimeField(verbose_name="Время")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    comment = models.TextField(blank=True, verbose_name="Комментарий клиента")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Запись"
        verbose_name_plural = "Записи"

    def __str__(self):
        return f"{self.client} — {self.service} — {self.date}"
