from django.db.models.signals import post_save

from finsys import models
from .account_balance_signal import AccountBalanceSignal
from .bank_transaction_signal import BankTransactionSignal

post_save.connect(AccountBalanceSignal.calculate_balance, sender=models.JournalEntryLineModel)
post_save.connect(BankTransactionSignal.add_loan_or_capital, sender=models.BankTransactionModel)