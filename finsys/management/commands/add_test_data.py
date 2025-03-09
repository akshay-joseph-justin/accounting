# yourapp/management/commands/add_example_data.py
from django.core.management.base import BaseCommand

from finsys.models import AccountModel


class Command(BaseCommand):
    help = 'Add example data to the AccountModel'

    def handle(self, *args, **kwargs):
        # Create example accounts
        account1 = AccountModel.objects.create(
            code='1001',
            name='Cash',
            account_type=AccountModel.DEBIT,
            is_active=True,
            description='Cash account'
        )

        account2 = AccountModel.objects.create(
            code='2001',
            name='Accounts Payable',
            account_type=AccountModel.CREDIT,
            is_active=True,
            description='Accounts payable to suppliers'
        )

        account3 = AccountModel.objects.create(
            code='3001',
            name='Owner’s Equity',
            account_type=AccountModel.CREDIT,
            is_active=True,
            description='Owner’s equity account'
        )

        account4 = AccountModel.objects.create(
            code='4001',
            name='Sales Revenue',
            account_type=AccountModel.CREDIT,
            is_active=True,
            description='Revenue from sales'
        )

        account5 = AccountModel.objects.create(
            code='5001',
            name='Office Supplies',
            account_type=AccountModel.DEBIT,
            is_active=True,
            description='Expenses for office supplies'
        )

        # Create a child account
        account6 = AccountModel.objects.create(
            code='1002',
            name='Petty Cash',
            account_type=AccountModel.DEBIT,
            parent=account1,
            is_active=True,
            description='Petty cash account'
        )

        self.stdout.write(self.style.SUCCESS('Successfully added example data to AccountModel'))
