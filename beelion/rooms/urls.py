from django.urls import path
from . import views

urlpatterns = [
    path('', views.rooms, name='rooms'),
    path('<int:pk>/', views.RoomDetailView.as_view(), name='room-detail'),
    path('add_room/', views.add_room, name='add_room'),
    path('manage_room/<int:pk>/', views.manage_room, name='manage_room'),
    path('select_room_for_edit/', views.select_room_for_edit, name='select_room_for_edit'),
    path('delete/<int:pk>/', views.delete_room, name='delete_room'),
]
