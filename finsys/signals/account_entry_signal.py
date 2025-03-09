from finsys.models import AccountModel


class AccountEntrySignal:

    @classmethod
    def process(cls, sender, instance, created, **kwargs):
        if created:
            account = AccountModel.objects.get(pk=instance.account.pk)
            print(f"{instance} - {instance.account.balance} : {account.balance}")
            account.balance += instance.credit_amount
            account.balance -= instance.debit_amount
            account.save()
            print(f"{instance} - {instance.account.balance} : {account.balance}")
