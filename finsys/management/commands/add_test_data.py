from datetime import datetime

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from finsys import models


class Command(BaseCommand):
    help = 'Add example datas'

    def add_accounts(self):
        account1 = models.AccountModel.objects.create(
            code='1001',
            name='Cash',
            account_type=models.AccountModel.DEBIT,
            is_active=True,
            description='Cash account'
        )

        account2 = models.AccountModel.objects.create(
            code='2001',
            name='Accounts Payable',
            account_type=models.AccountModel.CREDIT,
            is_active=True,
            description='Accounts payable to suppliers'
        )

        account3 = models.AccountModel.objects.create(
            code='3001',
            name='Owner’s Equity',
            account_type=models.AccountModel.CREDIT,
            is_active=True,
            description='Owner’s equity account'
        )

        account4 = models.AccountModel.objects.create(
            code='4001',
            name='Sales Revenue',
            account_type=models.AccountModel.CREDIT,
            is_active=True,
            description='Revenue from sales'
        )

        account5 = models.AccountModel.objects.create(
            code='5001',
            name='Office Supplies',
            account_type=models.AccountModel.DEBIT,
            is_active=True,
            description='Expenses for office supplies'
        )

        # Create a child account
        account6 = models.AccountModel.objects.create(
            code='1002',
            name='Petty Cash',
            account_type=models.AccountModel.DEBIT,
            parent=account1,
            is_active=True,
            description='Petty cash account'
        )

    def add_banks(self):
        models.BanKModel.objects.create(name="Cash")
        models.BanKModel.objects.create(name="SBI")

    def add_bank_transactions(self):
        cash = models.BanKModel.objects.get(name="Cash")
        sbi = models.BanKModel.objects.get(name="SBI")
        root = get_user_model().objects.get(username='root')

        models.BankTransactionModel.objects.create(
            bank=cash,
            user=root,
            date=datetime.now(),
            transaction_type=models.BankTransactionModel.LOAN,
            amount=10000
        )
        models.BankTransactionModel.objects.create(
            bank=cash,
            user=root,
            date=datetime.now(),
            transaction_type=models.BankTransactionModel.CAPITAL,
            amount=20000
        )
        models.BankTransactionModel.objects.create(
            bank=sbi,
            user=root,
            date=datetime.now(),
            transaction_type=models.BankTransactionModel.LOAN,
            amount=20000
        )
        models.BankTransactionModel.objects.create(
            bank=sbi,
            user=root,
            date=datetime.now(),
            transaction_type=models.BankTransactionModel.CAPITAL,
            amount=30000
        )

    def handle(self, *args, **kwargs):
        self.add_accounts()
        self.add_banks()
        self.add_bank_transactions()

        self.stdout.write(self.style.SUCCESS('Successfully added example data to models.AccountModel'))
