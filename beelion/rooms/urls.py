# rooms/urls.py
from django.urls import path
from . import views

app_name = 'rooms'  # Задаем пространство имен для приложения

urlpatterns = [
    path('', views.rooms, name='rooms'),
    path('<int:pk>/', views.RoomDetailView.as_view(), name='room-detail'),
    path('add_room/', views.add_room, name='add_room'),
    path('manage_room/<int:pk>/', views.manage_room, name='manage_room'),
    path('select_room_for_edit/', views.select_room_for_edit, name='select_room_for_edit'),
    path('delete/<int:pk>/', views.delete_room, name='delete_room'),
    path('book_room/<int:pk>/', views.book_room, name='book_room'),
    path('profile/', views.user_profile, name='user-profile'),
    path('cancel_booking/<int:pk>/', views.cancel_booking, name='cancel-booking'),
    path('services/', views.list_services, name='list_services'),  # Список всех услуг
    path('services/add/', views.add_service, name='add_service'),  # Добавить услугу
    path('services/edit/<int:service_id>/', views.edit_service, name='edit_service'),  # Редактировать услугу
    path('services/delete/<int:service_id>/', views.delete_service, name='delete_service'),  # Удалить услугу
    path('add_booking/', views.add_booking, name='add_booking'),
    path('edit_booking/<int:booking_id>/', views.edit_booking, name='edit_booking'),
    path('delete_booking/<int:booking_id>/', views.delete_booking, name='delete_booking'),
    path('list_bookings/', views.list_bookings, name='list_bookings'),
    path('add_admin_booking/', views.add_admin_booking, name='add_admin_booking'),
    path('<int:room_id>/', views.RoomDetailView.as_view(), name='room-detail'),  # подробности комнаты
    path('<int:room_id>/add_comment/', views.add_comment, name='add_comment'),  # добавление комментария



]
