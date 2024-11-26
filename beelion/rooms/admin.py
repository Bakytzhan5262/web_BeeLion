from django.contrib import admin
from .models import Room, Booking

# Регистрация модели Room
admin.site.register(Room)

# Проверяем, зарегистрирована ли Booking, и снимаем регистрацию, если нужно
if admin.site.is_registered(Booking):
    admin.site.unregister(Booking)

# Создаём класс для админки модели Booking
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'room', 'start_date', 'end_date', 'total_price')

    # Отображаем поле `total_price` в списке
    def total_price(self, obj):
        return obj.total_price
    total_price.short_description = 'Общая стоимость'

# Регистрируем модель Booking с админ-классом
admin.site.register(Booking, BookingAdmin)
