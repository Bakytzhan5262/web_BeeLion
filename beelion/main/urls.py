# main/urls.py
from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('contact', views.contact, name='contact'),
    path('admin-page/', views.admin_page, name='admin_page'),


]
