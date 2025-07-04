from django.contrib.auth import get_user_model
from django.db import models
from simple_history.models import HistoricalRecords
from finsys.utils import generate_random_number

from users.models import CompanyModel, YearModel

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

    company = models.ForeignKey(CompanyModel, on_delete=models.PROTECT)
    name = models.CharField(max_length=100)
    account_type = models.SmallIntegerField(choices=ACCOUNT_TYPES)
    balance = models.DecimalField(max_digits=20, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.name}"


class BankModel(TimeStampedModel):
    company = models.ForeignKey(CompanyModel, on_delete=models.PROTECT)
    name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=50, null=True, blank=True)
    branch = models.CharField(max_length=50, null=True, blank=True)
    balance = models.DecimalField(max_digits=20, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.branch} - {self.name} ({self.balance})"


class BankTransactionModel(TimeStampedModel):
    CREDIT = 1
    DEBIT = 2
    TYPES = (
        (CREDIT, 'Credit'),
        (DEBIT, 'Debit'),
    )

    year = models.ForeignKey(YearModel, on_delete=models.PROTECT)
    serial_number = models.CharField(max_length=100, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    bank = models.ForeignKey(BankModel, on_delete=models.PROTECT)
    date = models.DateField()
    head = models.CharField(max_length=50, null=True, blank=True)
    from_where = models.CharField(max_length=50, null=True, blank=True)
    transaction_type = models.SmallIntegerField(choices=TYPES)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    is_deleted = models.BooleanField(default=False)
    is_visible = models.BooleanField(default=True)
    foreign_id = models.IntegerField(null=True, blank=True)

    def save(self, **kwargs):
        if not self.serial_number:
            self.serial_number = generate_random_number()
        return super().save(**kwargs)


class LedgerModel(TimeStampedModel):
    company = models.ForeignKey(CompanyModel, on_delete=models.PROTECT)
    year = models.ForeignKey(YearModel, on_delete=models.PROTECT)
    serial_number = models.CharField(max_length=100, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    date = models.DateField()
    from_where = models.CharField(max_length=50)
    bank = models.ForeignKey(BankModel, on_delete=models.PROTECT, null=True, blank=True)
    amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    description = models.TextField(null=True, blank=True)
    history = HistoricalRecords(inherit=True)
    is_deleted = models.BooleanField(default=False)
    is_visible = models.BooleanField(default=True)

    class Meta:
        abstract = True

    def save(self, **kwargs):
        if not self.serial_number:
            self.serial_number = generate_random_number()
        return super().save(**kwargs)


class CapitalModel(TimeStampedModel):
    company = models.ForeignKey(CompanyModel, on_delete=models.PROTECT)
    year = models.ForeignKey(YearModel, on_delete=models.PROTECT)
    balance = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    first = models.DecimalField(max_digits=20, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        if self.first == 0:
            self.first = self.balance
        return super().save(*args, **kwargs)


class LoanModel(TimeStampedModel):
    company = models.ForeignKey(CompanyModel, on_delete=models.PROTECT)
    year = models.ForeignKey(YearModel, on_delete=models.PROTECT)
    balance = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    first = models.DecimalField(max_digits=20, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        if self.first == 0:
            self.first = self.balance
        return super().save(*args, **kwargs)


class CapitalHistoryModel(LedgerModel):

    def __str__(self):
        return f"Capital - {self.id} - {self.date}"


class LoanHistoryModel(LedgerModel):
    pending_amount = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    is_pay = models.BooleanField(default=False)

    def __str__(self):
        return f"Loan {self.id} - {self.date}"


class AccountHistoryModel(LedgerModel):
    account = models.ForeignKey(AccountModel, on_delete=models.PROTECT)

    def __str__(self):
        return f"Ac {self.id} - {self.date}"


class FixedAssetsModel(TimeStampedModel):
    company = models.ForeignKey(CompanyModel, on_delete=models.PROTECT)
    year = models.ForeignKey(YearModel, on_delete=models.PROTECT)
    balance = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    first = models.DecimalField(max_digits=20, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        if self.first == 0:
            self.first = self.balance
        return super().save(*args, **kwargs)


class FixedAssetsHistoryModel(LedgerModel):
    depreciation = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    current_balance = models.DecimalField(max_digits=20, decimal_places=2, default=0)

    def save(self, **kwargs):
        if self.current_balance == 0:
            self.current_balance = self.amount

        if self.depreciation > 0 and self.current_balance > 0:
            self.current_balance = self.amount - self.depreciation

        return super().save(**kwargs)

    def __str__(self):
        return f"{self.from_where}"


class DepreciationModel(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    date = models.DateField()
    asset = models.ForeignKey(FixedAssetsHistoryModel, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=20, decimal_places=2, default=0)


class JournalModel(LedgerModel):
    CREDIT = 1
    DEBIT = 2
    TYPES = (
        (CREDIT, 'Credit'),
        (DEBIT, 'Debit'),
    )

    transaction_type = models.SmallIntegerField(choices=TYPES)

    def __str__(self):
        return f"journal {self.id} - {self.date}"
