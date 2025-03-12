# models.py

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AccountModel(TimeStampedModel):
    CREDIT = 1
    DEBIT = 2
    ACCOUNT_TYPES = (
        (1, 'Credit'),
        (2, 'Debit'),
    )

    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    account_type = models.SmallIntegerField(choices=ACCOUNT_TYPES)
    balance = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    is_inbuilt = models.BooleanField(default=False)
    is_bank = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.code} - {self.name}"


class JournalEntryModel(TimeStampedModel):
    date = models.DateField()
    reference_number = models.CharField(max_length=50)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.date} - {self.reference_number}"


class JournalEntryLineModel(TimeStampedModel):
    DEBIT = 1
    CREDIT = 2
    ENTRY_TYPES = (
        (DEBIT, 'Debit'),
        (CREDIT, 'Credit'),
    )

    entry = models.ForeignKey(JournalEntryModel, related_name='lines', on_delete=models.CASCADE)
    account = models.ForeignKey(AccountModel, on_delete=models.PROTECT)
    entry_type = models.SmallIntegerField(choices=ENTRY_TYPES)
    amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.account.name}"
