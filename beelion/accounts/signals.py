from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

# Убедитесь, что нет обращения к атрибутам или моделям, которые могут отсутствовать
@receiver(post_save, sender=User)
def save_user_account(sender, instance, **kwargs):
    pass  # Оставьте пустым, если функционал не нужен
