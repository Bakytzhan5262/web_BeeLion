# accounts/models.py
from django.db import models

from decimal import Decimal

class Card(models.Model):
    card_number = models.CharField(max_length=16, unique=True)
    balance = models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self):
        return f"Карта {self.card_number} - Баланс: {self.balance}₽"

    def withdraw(self, amount):

        amount = Decimal(amount)

        if self.balance >= amount:
            self.balance -= amount
            self.save()
        else:
            raise ValueError("На карте недостаточно средств.")
