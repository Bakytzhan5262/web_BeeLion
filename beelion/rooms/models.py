from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta

class Room(models.Model):
    name = models.CharField('Названия', max_length=100)
    room_number = models.IntegerField('Номер комнаты')
    room_area = models.FloatField('Площадь')
    room_status = models.BooleanField('Статус')
    price = models.FloatField('Цена за сутки')
    number_of_people = models.IntegerField('Кол-во человек')
    image = models.ImageField('Изображение', upload_to='room_images/', null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.room_number}"

    class Meta:
        verbose_name = 'Комната'
        verbose_name_plural = 'Комнаты'


class Booking(models.Model):
    PAYMENT_METHODS = [
        ('cash', 'Наличные'),
        ('card', 'Карта'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    room = models.ForeignKey('Room', on_delete=models.CASCADE, verbose_name="Комната")
    start_date = models.DateField("Дата начала")
    end_date = models.DateField("Дата конца")
    phone_number = models.CharField("Номер телефона", max_length=15)
    payment_method = models.CharField("Тип оплаты", max_length=10, choices=PAYMENT_METHODS)
    services = models.TextField("Услуги", blank=True, null=True)
    total_price = models.FloatField("Общая стоимость", editable=False)  # Поле для хранения итоговой стоимости
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Вычисляем количество дней бронирования
        total_days = (self.end_date - self.start_date).days
        self.total_price = total_days * self.room.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Бронирование {self.room.name} от {self.start_date} до {self.end_date} - {self.user.username}"

    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"
