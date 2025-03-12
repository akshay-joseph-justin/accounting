from finsys.models import AccountModel, JournalEntryLineModel


class AccountBalanceSignals:

    @classmethod
    def calculate_balance(cls, sender, instance, created, **kwargs):
        if created:
            account = AccountModel.objects.get(pk=instance.account.pk)
            if instance.entry_type == JournalEntryLineModel.DEBIT:
                account.balance -= instance.amount

            if instance.entry_type == JournalEntryLineModel.CREDIT:
                account.balance += instance.amount

            account.save()
