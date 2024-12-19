from django import forms
from .models import Room, Booking, Service
import re


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'room_number', 'room_area', 'room_status', 'price', 'number_of_people', 'image']


class BookingForm(forms.ModelForm):
    card_number = forms.CharField(
        max_length=16,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Номер карты'})
    )

    class Meta:
        model = Booking
        fields = ['room', 'start_date', 'end_date', 'phone_number', 'payment_method', 'services', 'card_number']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'services': forms.CheckboxSelectMultiple(),  # Отображаем услуги как чекбоксы
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Получаем текущего пользователя из вызова формы
        super().__init__(*args, **kwargs)

        # Показываем только доступные комнаты
        self.fields['room'].queryset = Room.objects.filter(room_status=True)

        # Заполняем услуги из базы
        self.fields['services'].queryset = Service.objects.all()

    def clean_card_number(self):
        card_number = self.cleaned_data.get('card_number')
        payment_method = self.cleaned_data.get('payment_method')

        # Если выбрана оплата картой, то номер карты обязателен
        if payment_method == 'card':
            if not card_number:
                raise forms.ValidationError("Номер карты обязателен при выборе оплаты картой.")

            # Проверка на корректность номера карты (например, 16 цифр)
            if not re.match(r'^\d{16}$', card_number):
                raise forms.ValidationError("Номер карты должен содержать 16 цифр.")

        return card_number


from django import forms
from .models import Service

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'price']


from django import forms
from django.contrib.auth.models import User
from .models import Booking, Room, Service

class AdminBookingForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.all(), label="Пользователь")
    room = forms.ModelChoiceField(queryset=Room.objects.all(), label="Комната")
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Дата начала")
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Дата конца")
    phone_number = forms.CharField(max_length=15, label="Номер телефона", widget=forms.TextInput(attrs={'placeholder': 'Введите номер телефона'}))
    services = forms.ModelMultipleChoiceField(
        queryset=Service.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Услуги"
    )
    payment_method = forms.ChoiceField(
        choices=[('cash', 'Наличные'), ('card', 'Карта')],
        widget=forms.RadioSelect,
        label="Способ оплаты"
    )

    class Meta:
        model = Booking
        fields = ['user', 'room', 'start_date', 'end_date', 'phone_number', 'services', 'payment_method']



# forms.py
from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'rating']  # Параметры комментария

    content = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Your review here...', 'required': True}))
    rating = forms.ChoiceField(choices=[(i, i) for i in range(1, 6)], widget=forms.RadioSelect)


