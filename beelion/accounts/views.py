# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .forms import UserRegisterForm
from django.contrib.auth.forms import UserCreationForm  # Если вы хотите использовать стандартную форму
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .forms import UserRegisterForm
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import logout
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash


# Функция для регистрации
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Аккаунт {username} создан! Теперь вы можете войти.')
            return redirect('login')
        else:
            messages.error(request, 'Ошибка при регистрации. Проверьте введенные данные.')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

# Функция для входа
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Вы успешно вошли!')
            return redirect('index')  # Перенаправление на главную страницу
        else:
            messages.error(request, 'Неверный логин или пароль.')

    return render(request, 'accounts/login.html')

@user_passes_test(lambda u: u.is_staff)
def add_user(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Пользователь успешно добавлен.')
            return redirect('admin_page')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/add_user.html', {'form': form})

@user_passes_test(lambda u: u.is_staff)  # Только для администраторов
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        # Обработка редактирования пользователя
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirmation = request.POST.get('password_confirmation')

        # Обновление данных пользователя
        user.username = username
        user.email = email

        # Проверка и обновление пароля, если введен новый
        if password and password == password_confirmation:
            user.set_password(password)

        user.save()

        # Обновляем сессию после изменения пароля
        if password:
            update_session_auth_hash(request, user)

        messages.success(request, 'Пользователь успешно обновлен.')  # Сообщение об успешном редактировании
        return redirect('edit_user', user_id=user.id)

    return render(request, 'accounts/edit_user.html', {'user': user})


def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        user.delete()
        messages.success(request, 'Пользователь успешно удален.')  # Сообщение об успешном удалении
        return redirect('select_user')

    return redirect('select_user')  # или другая страница, если хотите


def select_user(request):
    # Получаем всех пользователей
    users = User.objects.all()
    return render(request, 'accounts/select_user.html', {'users': users})


def logout_view(request):
    logout(request)
    return redirect('login')


from .forms import CardForm
from .models import Card

def process_payment(request):
    if request.method == 'POST':
        form = CardForm(request.POST)
        if form.is_valid():
            card_number = form.cleaned_data['card_number']
            amount = form.cleaned_data['amount']

            # Получаем карту и снимаем деньги
            card = Card.objects.get(card_number=card_number)
            try:
                card.withdraw(amount)
                return render(request, 'success.html', {'amount': amount})
            except ValueError as e:
                form.add_error(None, str(e))
    else:
        form = CardForm()
    return render(request, 'payment.html', {'form': form})