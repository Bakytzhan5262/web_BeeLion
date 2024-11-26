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
]