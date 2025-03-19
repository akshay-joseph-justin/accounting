from django.contrib.auth import get_user_model
from django.db import models
from simple_history.models import HistoricalRecords

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

    name = models.CharField(max_length=100)
    account_type = models.SmallIntegerField(choices=ACCOUNT_TYPES)
    balance = models.DecimalField(max_digits=20, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.name}"


class BankModel(TimeStampedModel):
    name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=50, null=True, blank=True)
    branch = models.CharField(max_length=50, null=True, blank=True)
    balance = models.DecimalField(max_digits=20, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.branch} - {self.name}"


class BankTransactionModel(TimeStampedModel):
    CREDIT = 1
    DEBIT = 2
    TYPES = (
        (CREDIT, 'Credit'),
        (DEBIT, 'Debit'),
    )

    user = models.ForeignKey(User, on_delete=models.PROTECT)
    bank = models.ForeignKey(BankModel, on_delete=models.PROTECT)
    date = models.DateField()
    head = models.CharField(max_length=50, null=True, blank=True)
    from_where = models.CharField(max_length=50, null=True, blank=True)
    transaction_type = models.SmallIntegerField(choices=TYPES)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    is_deleted = models.BooleanField(default=False)
    foreign_id = models.IntegerField(null=True, blank=True)


class LedgerModel(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    date = models.DateField()
    from_where = models.CharField(max_length=50)
    bank = models.ForeignKey(BankModel, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    description = models.TextField(null=True, blank=True)
    history = HistoricalRecords(inherit=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True


class CapitalModel(TimeStampedModel):
    balance = models.DecimalField(max_digits=20, decimal_places=2, default=0)


class LoanModel(TimeStampedModel):
    balance = models.DecimalField(max_digits=20, decimal_places=2, default=0)


class CapitalHistoryModel(LedgerModel):

    def __str__(self):
        return f"{self.date} - {self.bank}"


class LoanHistoryModel(LedgerModel):

    def __str__(self):
        return f"{self.date} - {self.bank}"


class AccountHistoryModel(LedgerModel):
    account = models.ForeignKey(AccountModel, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.date} - {self.bank}"


class FixedAssetsModel(TimeStampedModel):
    balance = models.DecimalField(max_digits=20, decimal_places=2, default=0)


class FixedAssetsHistoryModel(LedgerModel):
    depreciation = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    current_balance = models.DecimalField(max_digits=20, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        if self.current_balance == 0:
            self.current_balance = self.amount

        if self.depreciation > 0 and self.current_balance > 0:
            self.current_balance = self.amount - self.depreciation

        return super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.date} - {self.bank}"
