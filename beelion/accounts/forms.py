# accounts/forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Card


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class CardForm(forms.Form):
    card_number = forms.CharField(max_length=16, widget=forms.TextInput(attrs={'placeholder': 'Введите номер карты'}))
    amount = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'placeholder': 'Введите сумму'}))

    def clean_card_number(self):
        card_number = self.cleaned_data.get('card_number')
        if not Card.objects.filter(card_number=card_number).exists():
            raise forms.ValidationError("Неверный номер карты.")
        return card_number

    def clean(self):
        cleaned_data = super().clean()
        card_number = cleaned_data.get('card_number')
        amount = cleaned_data.get('amount')

        if card_number and amount:
            card = Card.objects.get(card_number=card_number)
            if card.balance < amount:
                raise forms.ValidationError("На карте недостаточно средств.")