from django.forms import ValidationError

from finsys.models import BankModel, BankTransactionModel


class BankSignal:

    @classmethod
    def change_balance(cls, sender, instance, created, **kwargs):
        if instance.is_deleted:
            return
        bank = BankModel.objects.get(pk=instance.bank.pk)
        if instance.transaction_type == BankTransactionModel.CREDIT:
            bank.balance += instance.amount

        if instance.transaction_type == BankTransactionModel.DEBIT:
            bank.balance -= instance.amount

        bank.save()

    @classmethod
    def pre_save(cls, sender, instance, **kwargs):
        bank = BankModel.objects.get(pk=instance.bank.pk)
        if bank.balance < instance.amount:
            return ValidationError("Bank Balance is lower than required amount")

