from django.db.models import Sum

from finsys.models import AccountModel, JournalEntryLineModel


class AccountBalanceSignal:

    @classmethod
    def calculate_balance(cls, sender, instance, created, **kwargs):
        if created:
            account = AccountModel.objects.get(pk=instance.account.pk)
            aggregated = JournalEntryLineModel.objects.filter(account=account).aggregate(
                total_debit=Sum('debit_amount', default=0),
                total_credit=Sum('credit_amount', default=0)
            )
            account.balance = aggregated['total_debit'] - aggregated['total_credit']
            account.save()
