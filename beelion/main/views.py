# main/views.py
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


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Comment
from .forms import CommentForm


from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import MessageForm


def contact_view(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ваше сообщение отправлено успешно!')
            return redirect('contact')  # Замените на ваш URL-нейм
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = MessageForm()

    return render(request, 'main/contact.html', {'form': form})

