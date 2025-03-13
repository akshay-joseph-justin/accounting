from datetime import datetime

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from finsys import models


class Command(BaseCommand):
    help = 'Add example datas'

    def add_accounts(self):

        models.AccountModel.objects.create(
            code='2001',
            name='Capital',
            account_type=models.AccountModel.CREDIT,
            is_inbuilt=True,
        )

        models.AccountModel.objects.create(
            code='3001',
            name='Loan',
            account_type=models.AccountModel.CREDIT,
            is_inbuilt=True,
        )

        models.AccountModel.objects.create(
            code='4001',
            name='Fixed Assets',
            account_type=models.AccountModel.DEBIT,
            is_inbuilt=True,
        )

        models.AccountModel.objects.create(
            code='5001',
            name='Income',
            account_type=models.AccountModel.CREDIT,
            is_inbuilt=True,
        )

        models.AccountModel.objects.create(
            code='1002',
            name='Expense',
            account_type=models.AccountModel.DEBIT,
            is_inbuilt=True,
        )
        models.AccountModel.objects.create(
            code='2112',
            name='Cash',
            account_type=models.AccountModel.CREDIT,
            is_bank=True
        )

    def handle(self, *args, **kwargs):
        self.add_accounts()

        self.stdout.write(self.style.SUCCESS('Successfully added example data to models.AccountModel'))
