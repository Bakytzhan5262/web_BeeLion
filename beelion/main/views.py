from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from rooms.models import Room

def index(request):
    return render(request, 'main/index.html')
def contact(request):
    return render(request, 'main/contact.html')

@user_passes_test(lambda u: u.is_staff)
def admin_page(request):
    rooms = Room.objects.all()  # Получаем все комнаты
    return render(request, 'main/admin_page.html', {'rooms': rooms})

