from django.db.models.signals import post_save

from finsys import models
from .account_entry_signal import AccountEntrySignal

post_save.connect(AccountEntrySignal.process, sender=models.JournalEntryLineModel)
