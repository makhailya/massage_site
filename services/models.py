from django.db import models


class Service(models.Model):
    # Тип массажа — выбор из списка
    TYPE_CHOICES = [
        ('classic', 'Оздоровительный'),
        ('relax', 'Релакс '),
        ('home', 'Выезд на дом'),
    ]

    name = models.CharField(max_length=200)  # Название услуги
    service_type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES
    )
    description = models.TextField()  # Описание
    price = models.PositiveIntegerField()  # Цена в рублях
    duration = models.PositiveIntegerField()  # Длительность в минутах
    is_active = models.BooleanField(default=True)  # Показывать на сайте?

    def __str__(self):
        return f"{self.name} — {self.price} руб."  # Как выглядит в админке

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'
