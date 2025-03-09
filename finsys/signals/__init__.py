from django.db.models.signals import post_save

from finsys import models
from .account_balance_signal import AccountBalanceSignal

post_save.connect(AccountBalanceSignal.calculate_balance, sender=models.JournalEntryLineModel)
