from django import forms
from .models import Room

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'room_number', 'room_area', 'room_status', 'price', 'number_of_people', 'image']
