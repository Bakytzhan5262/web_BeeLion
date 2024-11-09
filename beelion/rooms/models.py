from django.db import models

class Room(models.Model):
    name = models.CharField('Названия',max_length=100)
    room_number = models.IntegerField('Номер комнаты')
    room_area = models.FloatField('Площадь')
    room_status = models.BooleanField('Статус')
    price = models.FloatField('Цена')
    number_of_people = models.IntegerField('Кол-во человек')
    image = models.ImageField('Изображение', upload_to='room_images/', null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.room_number}"

    class Meta:
        verbose_name = 'Комната'
        verbose_name_plural = 'Комнаты'