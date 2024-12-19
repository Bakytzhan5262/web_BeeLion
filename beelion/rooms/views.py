# rooms/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Room
from django.views.generic import DetailView
from .forms import RoomForm
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import Booking,Service
from accounts.models import Card
from django.contrib import messages
from decimal import Decimal

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




from django.contrib import messages

from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Room, Service
from .forms import BookingForm


@login_required
def book_room(request, pk):
    room = get_object_or_404(Room, pk=pk)

    if request.method == 'POST':
        form = BookingForm(request.POST, user=request.user)
        if form.is_valid():
            start_date = form.cleaned_data.get('start_date')
            end_date = form.cleaned_data.get('end_date')
            selected_services = form.cleaned_data.get('services')

            # Проверка корректности дат
            if not start_date or not end_date or end_date <= start_date:
                messages.error(request, "Неверные даты бронирования.")
                return render(request, 'rooms/book_room.html', {'room': room, 'form': form})

            # Рассчитываем стоимость
            number_of_days = (end_date - start_date).days
            room_total_price = room.price * number_of_days
            services_total_price = sum([service.price for service in selected_services])
            total_price = room_total_price + services_total_price

            # Сохраняем бронирование
            booking = form.save(commit=False)
            booking.user = request.user
            booking.room = room
            booking.total_price = total_price
            booking.save()

            # Устанавливаем услуги (если есть)
            if selected_services:
                booking.services.set(selected_services)

            # Уведомление об успешном бронировании
            messages.success(request, f"Бронирование комнаты '{room.name}' успешно создано!")

            # Перенаправляем пользователя в профиль
            return redirect('rooms:user-profile')  # Исправлено на правильное имя маршрута
 # Перенаправление на профиль пользователя

        else:
            messages.error(request, "Произошла ошибка при заполнении формы.")

    else:
        form = BookingForm(user=request.user)

    services = Service.objects.all()
    return render(request, 'rooms/book_room.html', {'room': room, 'form': form, 'services': services})


from django.utils import timezone

from django.utils.timezone import now

from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Booking

@login_required
def user_profile(request):
    user = request.user
    today = timezone.now().date()

    # Фильтруем все бронирования пользователя
    bookings = Booking.objects.filter(user=user).order_by('-start_date')

    # Активные бронирования
    active_bookings = Booking.objects.filter(
        user=user,
        start_date__lte=today,
        end_date__gte=today,
        is_canceled=False
    ).order_by('start_date')

    # Предстоящие бронирования
    upcoming_bookings = Booking.objects.filter(
        user=user,
        start_date__gt=today,
        is_canceled=False
    ).order_by('start_date')

    # Завершённые бронирования
    completed_bookings = Booking.objects.filter(
        user=user,
        end_date__lt=today,
        is_canceled=False
    ).order_by('-end_date')

    # Отменённые бронирования
    canceled_bookings = Booking.objects.filter(
        user=user,
        is_canceled=True
    ).order_by('-start_date')

    return render(request, 'rooms/user_profile.html', {
        'user': user,
        'active_bookings': active_bookings,
        'upcoming_bookings': upcoming_bookings,
        'completed_bookings': completed_bookings,
        'canceled_bookings': canceled_bookings,
        'today': today,
    })






from django.http import JsonResponse
from django.utils import timezone


from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Booking

@login_required
def cancel_booking(request, pk):
    if request.method == "POST":
        booking = get_object_or_404(Booking, pk=pk, user=request.user)

        # Проверяем, не началась ли еще дата бронирования
        if booking.start_date <= timezone.now().date():
            return JsonResponse(
                {"success": False, "error": "Невозможно отменить бронирование, которое уже началось или завершено."})

        # Обновляем статус бронирования на "отменено"
        booking.is_canceled = True
        booking.save()

        return JsonResponse({"success": True})

    return JsonResponse({"success": False, "error": "Неверный запрос."}, status=400)

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from .models import Service
from .forms import ServiceForm

# Функция для проверки прав администратора
def is_admin(user):
    return user.is_staff

# Страница для добавления новой услуги
@user_passes_test(is_admin)
def add_service(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('rooms:list_services')  # Перенаправление на список услуг
    else:
        form = ServiceForm()
    return render(request, 'rooms/add_service.html', {'form': form})

# Страница для редактирования существующей услуги
@user_passes_test(is_admin)
def edit_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            return redirect('rooms:list_services')  # Перенаправление на список услуг
    else:
        form = ServiceForm(instance=service)
    return render(request, 'rooms/edit_service.html', {'form': form, 'service': service})

# Страница для удаления услуги
@user_passes_test(is_admin)
def delete_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    if request.method == 'POST':
        service.delete()
        return redirect('rooms:list_services')  # Перенаправление на список услуг
    return render(request, 'rooms/delete_service.html', {'service': service})

# Страница для отображения всех услуг
@user_passes_test(is_admin)
def list_services(request):
    services = Service.objects.all()
    return render(request, 'rooms/list_services.html', {'services': services})

@user_passes_test(lambda u: u.is_staff)
def add_booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Бронирование успешно добавлено!")
            return redirect('rooms:list_bookings')  # Перенаправление на список бронирований
    else:
        form = BookingForm()
    return render(request, 'rooms/add_booking.html', {'form': form})


@user_passes_test(lambda u: u.is_staff)
def edit_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            messages.success(request, "Бронирование успешно обновлено!")
            return redirect('rooms:list_bookings')  # Перенаправление на список бронирований
    else:
        form = BookingForm(instance=booking)
    return render(request, 'rooms/edit_booking.html', {'form': form, 'booking': booking})


@user_passes_test(lambda u: u.is_staff)
def delete_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if request.method == 'POST':
        booking.delete()
        messages.success(request, "Бронирование удалено!")
        return redirect('rooms:list_bookings')  # Перенаправление на список бронирований
    return render(request, 'rooms/delete_booking.html', {'booking': booking})



@user_passes_test(lambda u: u.is_staff)
def list_bookings(request):
    bookings = Booking.objects.all()
    return render(request, 'rooms/list_bookings.html', {'bookings': bookings})


from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Sum
from .forms import AdminBookingForm
from .models import Booking

from django.contrib import messages
from django.shortcuts import render, redirect
from django.db.models import Sum
from .forms import AdminBookingForm
from .models import Service

def add_admin_booking(request):
    if not request.user.is_staff:  # Проверяем, что это администратор
        messages.error(request, "Доступ запрещен.")
        return redirect('rooms:rooms')

    if request.method == "POST":
        form = AdminBookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)

            # Рассчитываем цену за комнату
            room_price = booking.room.price
            start_date = booking.start_date
            end_date = booking.end_date
            days = (end_date - start_date).days

            if days < 1:
                messages.error(request, "Дата окончания должна быть позже даты начала.")
                return render(request, 'rooms/admin_add_booking.html', {'form': form})

            room_total = room_price * days

            # Рассчитываем цену за услуги
            services = form.cleaned_data['services']
            services_total = services.aggregate(Sum('price'))['price__sum'] or 0

            # Общая цена
            booking.total_price = room_total + services_total

            # Сохраняем бронирование
            booking.save()
            form.save_m2m()  # Сохраняем связи Many-to-Many (услуги)

            messages.success(request, "Бронирование успешно добавлено.")
            return redirect('rooms:list_bookings')
    else:
        form = AdminBookingForm()

    return render(request, 'rooms/admin_add_booking.html', {'form': form})



# views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Room, Comment
from .forms import CommentForm

def room_detail(request, pk):
    room = get_object_or_404(Room, pk=pk)  # Получаем комнату по id
    comments = room.comments.all()  # Все комментарии к комнате
    form = CommentForm(request.POST or None)  # Создаем форму для комментариев

    if request.method == 'POST' and form.is_valid() and request.user.is_authenticated:
        comment = form.save(commit=False)  # Не сохраняем сразу
        comment.user = request.user  # Присваиваем пользователя
        comment.room = room  # Присваиваем комнату
        comment.save()  # Сохраняем комментарий
        return redirect('rooms:room-detail', pk=room.pk)  # Перезагружаем страницу

    return render(request, 'rooms/room-details.html', {'room': room, 'comments': comments, 'form': form})

from django.shortcuts import render, get_object_or_404, redirect
from .models import Room, Comment
from .forms import CommentForm

def add_comment(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.method == 'POST':
        comment = Comment(
            user=request.user,
            room=room,
            text=request.POST['text']
        )
        comment.save()
        return redirect('rooms:room-detail', room_id=room.id)
    return redirect('rooms:room-detail', room_id=room.id)
