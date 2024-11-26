# rooms/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Room
from django.views.generic import DetailView
from .forms import RoomForm
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import Booking
from accounts.models import Card
from django.contrib import messages


from .forms import BookingForm


from datetime import datetime
def rooms(request):
    rooms = Room.objects.all()
    return render(request, 'rooms/rooms.html', {'rooms': rooms})

class RoomDetailView(DetailView):
    model = Room
    template_name = 'rooms/room-details.html'
    context_object_name = 'room'

# Вынесем функцию add_room вне класса
@user_passes_test(lambda u: u.is_staff)
def add_room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_page')  # Перенаправление на админ-панель
    else:
        form = RoomForm()
    return render(request, 'rooms/add_room.html', {'form': form})


@user_passes_test(lambda u: u.is_staff)
def manage_room(request, pk):
    room = get_object_or_404(Room, pk=pk)

    if request.method == 'POST':
        if 'edit' in request.POST:  # Обработка редактирования
            form = RoomForm(request.POST, request.FILES, instance=room)
            if form.is_valid():
                form.save()
                return redirect('room-detail', pk=room.pk)
        elif 'delete' in request.POST:  # Обработка удаления
            room.delete()
            return redirect('admin_page')  # Перенаправление на админ-панель после удаления
    else:
        form = RoomForm(instance=room)

    return render(request, 'rooms/manage_room.html', {'form': form, 'room': room})


from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Room

def rooms_view(request):
    rooms_list = Room.objects.all()  # Все комнаты из базы данных
    print("Rooms count:", rooms_list.count())  # Вывод количества комнат в консоль
    paginator = Paginator(rooms_list, 4)  # 4 комнаты на странице
    page_number = request.GET.get('page')  # Получаем номер страницы из параметров GET
    rooms = paginator.get_page(page_number)  # Получаем список комнат для текущей страницы

    return render(request, 'rooms/rooms.html', {'rooms': rooms})

def manage_room(request, pk):
    room = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES, instance=room)
        if form.is_valid():
            form.save()
            return redirect('admin_page')  # Или другая нужная страница
    else:
        form = RoomForm(instance=room)  # Заполняем форму данными комнаты

    return render(request, 'rooms/manage_room.html', {'room': room, 'form': form})

def select_room_for_edit(request):
    rooms = Room.objects.all()
    return render(request, 'rooms/select_room_for_edit.html', {'rooms': rooms})

def delete_room(request, pk):
    room = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('admin_page')
    return redirect('manage_room', pk=pk)


@login_required
def book_room(request, pk):
    room = get_object_or_404(Room, pk=pk)

    if request.method == 'POST':
        form = BookingForm(request.POST, user=request.user)
        if form.is_valid():
            start_date = form.cleaned_data.get('start_date')
            end_date = form.cleaned_data.get('end_date')

            if not start_date or not end_date:
                messages.error(request, "Вы должны указать даты начала и окончания.")
                return render(request, 'rooms/book_room.html', {'room': room, 'form': form})

            # Проверяем, что дата окончания позже даты начала
            if end_date <= start_date:
                messages.error(request, "Дата окончания должна быть позже даты начала.")
                return render(request, 'rooms/book_room.html', {'room': room, 'form': form})

            # Рассчитываем стоимость
            number_of_days = (end_date - start_date).days
            total_price = number_of_days * room.price

            # Если оплата картой
            card_number = form.cleaned_data.get('card_number')
            payment_method = form.cleaned_data.get('payment_method')

            if payment_method == 'card' and card_number:
                # Ищем или создаем карту
                card, created = Card.objects.get_or_create(card_number=card_number)

                # Проверяем баланс карты
                if card.balance < total_price:
                    messages.error(request, "На вашей карте недостаточно средств.")
                    return render(request, 'rooms/book_room.html', {'room': room, 'form': form})

                # Снимаем деньги с карты
                card.withdraw(total_price)

            # Создаем бронирование
            booking = form.save(commit=False)
            booking.user = request.user
            booking.room = room
            booking.total_price = total_price
            booking.save()

            messages.success(request, "Бронирование успешно создано!")
            return redirect('rooms:room-detail', pk=room.pk)

    else:
        form = BookingForm(user=request.user)

    return render(request, 'rooms/book_room.html', {'room': room, 'form': form})