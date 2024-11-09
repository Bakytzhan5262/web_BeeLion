from django import template

register = template.Library()

@register.filter
def add_class(value, arg):
    """Добавляет класс к полю формы"""
    return value.as_widget(attrs={'class': arg})
