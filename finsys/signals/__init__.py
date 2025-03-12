from django.db.models.signals import post_save

from finsys import models
from .account_balance_signals import AccountBalanceSignals

post_save.connect(AccountBalanceSignals.calculate_balance, sender=models.JournalEntryLineModel)
