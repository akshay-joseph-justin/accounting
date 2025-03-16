from finsys.models import BankModel, BankTransactionModel


class BankSignal:

    @classmethod
    def change_balance(cls, sender, instance, created, **kwargs):
        bank = BankModel.objects.get(pk=instance.bank.pk)
        if instance.transaction_type == BankTransactionModel.CREDIT:
            bank.balance += instance.amount

        if instance.transaction_type == BankTransactionModel.DEBIT:
            bank.balance -= instance.amount

        if created:
            print("created")
        else:
            print("updated")

        print(f"{bank.name} - {instance.get_transaction_type_display()}: {instance.amount}")
        bank.save()

    @classmethod
    def delete(cls, sender, instance, created, **kwargs):
        if not created:
            transaction = BankTransactionModel.objects.get(pk=instance.pk)
            transaction.objects.update(is_deleted=True)
