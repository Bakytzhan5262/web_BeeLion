# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .forms import UserRegisterForm
from django.contrib.auth.forms import UserCreationForm  # Если вы хотите использовать стандартную форму
from django.contrib.auth.decorators import login_required

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
