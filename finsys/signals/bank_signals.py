from finsys.models import BankModel, BankTransactionModel


class BankSignal:

    @classmethod
    def change_balance(cls, sender, instance, created, **kwargs):
        bank = BankModel.objects.get(pk=instance.bank.pk)
        if instance.transaction_type == BankTransactionModel.CREDIT:
            bank.balance += instance.amount

        if instance.transaction_type == BankTransactionModel.DEBIT:
            bank.balance -= instance.amount

        bank.save()
