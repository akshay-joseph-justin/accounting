from django.forms import ValidationError

from finsys.models import BankModel, BankTransactionModel


class BankSignal:

    @classmethod
    def change_balance(cls, sender, instance, created, **kwargs):
        bank = BankModel.objects.get(pk=instance.bank.pk)
        if instance.transaction_type == BankTransactionModel.CREDIT:
            bank.balance += instance.amount

        if instance.transaction_type == BankTransactionModel.DEBIT:
            if bank.balance < instance.amount:
                return ValidationError("Bank Balance is lower than required amount")

            bank.balance -= instance.amount

        bank.save()

    @classmethod
    def delete(cls, sender, instance, created, **kwargs):
        if not created:
            transaction = BankTransactionModel.objects.get(pk=instance.pk)
            transaction.objects.update(is_deleted=True)
