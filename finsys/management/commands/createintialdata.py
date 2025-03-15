from datetime import datetime

from django.core.management.base import BaseCommand

from finsys import models


class Command(BaseCommand):
    help = 'Add example datas'

    def handle(self, *args, **kwargs):
        models.CapitalModel.objects.create()
        models.LoanModel.objects.create()
        models.FixedAssetsModel.objects.create()

        self.stdout.write(self.style.SUCCESS('Successfully added example data to models.AccountModel'))
