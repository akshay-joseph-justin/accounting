# models.py

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models


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
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    is_active = models.BooleanField(default=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.code} - {self.name}"


class FiscalPeriodModel(TimeStampedModel):
    name = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    is_closed = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class JournalEntry(TimeStampedModel):
    ENTRY_STATUS = (
        ('draft', 'Draft'),
        ('posted', 'Posted'),
        ('voided', 'Voided'),
    )

    date = models.DateField()
    reference_number = models.CharField(max_length=50)
    description = models.TextField()
    period = models.ForeignKey(FiscalPeriodModel, on_delete=models.PROTECT)
    status = models.CharField(max_length=20, choices=ENTRY_STATUS, default='draft')
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    posted_at = models.DateTimeField(null=True, blank=True)

    def clean(self):
        if self.period.is_closed:
            raise ValidationError("Cannot create entry in closed period")

    def __str__(self):
        return f"{self.date} - {self.reference_number}"


class JournalEntryLineModel(TimeStampedModel):
    entry = models.ForeignKey(JournalEntry, related_name='lines', on_delete=models.CASCADE)
    account = models.ForeignKey(AccountModel, on_delete=models.PROTECT)
    description = models.TextField(blank=True)
    debit_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    credit_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.account.name}"
