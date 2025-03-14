from django.core.management.base import BaseCommand

from finsys import models

class Command(BaseCommand):
    help = 'Add example datas'

    def handle(self, *args, **kwargs):
        models.BankModel.objects.create(
            name="SBI",
            account_number="123456",
            branch="kalala"
        )

        self.stdout.write(self.style.SUCCESS('Successfully added example data to models.AccountModel'))
