from django import forms
from .models import Room, Booking
import re


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'room_number', 'room_area', 'room_status', 'price', 'number_of_people', 'image']


from django import forms
from .models import Room, Booking
import re

class BookingForm(forms.ModelForm):
    card_number = forms.CharField(max_length=16, required=False, widget=forms.TextInput(attrs={'placeholder': 'Номер карты'}))
    payment_method = forms.ChoiceField(choices=[('cash', 'Наличные'), ('card', 'Карта')])

    class Meta:
        model = Booking
        fields = ['room', 'start_date', 'end_date', 'phone_number', 'payment_method', 'services', 'card_number']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'services': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Получаем текущего пользователя из вызова формы
        super().__init__(*args, **kwargs)

        # Если пользователь передан, автоматически задаём его email
        if user and user.is_authenticated:
            self.fields['room'].queryset = Room.objects.filter(room_status=True)  # Показываем только доступные комнаты

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