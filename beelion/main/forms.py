from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Имя', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control'}),
            'message': forms.Textarea(attrs={'placeholder': 'Сообщение', 'class': 'form-control', 'rows': 4}),
        }
        labels = {
            'name': '',
            'email': '',
            'message': '',
        }
from django import forms
from .models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['name', 'email', 'content']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Введите ваше имя',
                'class': 'form-control',
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Введите ваш email',
                'class': 'form-control',
            }),
            'content': forms.Textarea(attrs={
                'placeholder': 'Введите ваше сообщение',
                'class': 'form-control',
                'rows': 4,
            }),
        }
        labels = {
            'name': '',
            'email': '',
            'content': '',
        }
