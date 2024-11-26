# accounts/urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('select-user/', views.select_user, name='select_user'),  # Страница выбора пользователя
    path('edit-user/<int:user_id>/', views.edit_user, name='edit_user'),  # Страница редактирования пользователя
    path('add-user/', views.add_user, name='add_user'),
path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),

]