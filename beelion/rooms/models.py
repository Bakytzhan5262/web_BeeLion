from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

class Room(models.Model):
    name = models.CharField('Название', max_length=100)
    room_number = models.IntegerField('Номер комнаты')
    room_area = models.FloatField('Площадь')
    room_status = models.BooleanField('Статус', default=True)
    price = models.DecimalField('Цена за сутки', max_digits=10, decimal_places=2)  # Используем Decimal
    number_of_people = models.IntegerField('Кол-во человек')
    image = models.ImageField('Изображение', upload_to='room_images/', null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.room_number}"

    class Meta:
        verbose_name = 'Комната'
        verbose_name_plural = 'Комнаты'


class Service(models.Model):
    name = models.CharField("Название услуги", max_length=100)
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} ({self.price} тенге.)"

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"


from decimal import Decimal
from django.contrib.auth.models import User
from django.db import models

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
    services = models.ManyToManyField('Service', blank=True, verbose_name="Дополнительные услуги")
    total_price = models.DecimalField("Общая стоимость", max_digits=10, decimal_places=2, editable=False)
    is_canceled = models.BooleanField("Отменено", default=False)  # Поле для отслеживания отмены
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """
        Переопределяем метод сохранения для подсчёта общей стоимости бронирования.
        """
        if not self.pk:  # Если объект создаётся впервые
            super().save(*args, **kwargs)  # Сохраняем, чтобы получить ID

        # Рассчитываем общую стоимость
        total_days = (self.end_date - self.start_date).days
        room_cost = Decimal(self.room.price) * Decimal(total_days)
        services_cost = sum(Decimal(service.price) for service in self.services.all())

        # Устанавливаем общую стоимость
        self.total_price = room_cost + services_cost

        super().save(*args, **kwargs)  # Повторное сохранение с обновлённой стоимостью

    def __str__(self):
        status = "Отменено" if self.is_canceled else "Активно"
        return f"Бронирование {self.room.name} ({self.start_date} - {self.end_date}) - {self.user.username} ({status})"

    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"



# models.py
from django.db import models
from django.contrib.auth.models import User
from .models import Room

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, related_name='comments', on_delete=models.CASCADE)
    text = models.TextField()  # Это поле для текста комментария
    created_at = models.DateTimeField(auto_now_add=True)

