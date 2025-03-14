from django.db.models.signals import post_save, pre_save

from finsys import models
from .account_balance_signals import AccountBalanceSignals
from .bank_signals import BankSignal
from .capital_signals import CapitalSignal
from .loan_signals import LoanSignal

post_save.connect(AccountBalanceSignals.calculate_balance, sender=models.JournalEntryLineModel)
post_save.connect(BankSignal.change_balance, sender=models.BankTransactionModel)

post_save.connect(CapitalSignal.post_change_balance, sender=models.CapitalHistoryModel)
pre_save.connect(CapitalSignal.pre_change_balance, sender=models.CapitalHistoryModel)

post_save.connect(LoanSignal.post_change_balance, sender=models.LoanHistoryModel)
pre_save.connect(LoanSignal.pre_change_balance, sender=models.LoanHistoryModel)
