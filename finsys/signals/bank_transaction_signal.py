from finsys.models import BanKModel, BankTransactionModel


class BankTransactionSignal:

    @classmethod
    def add_loan_or_capital(cls, sender, instance, created, **kwargs):
        if created:
            bank = BanKModel.objects.get(pk=instance.bank.pk)
            if instance.transaction_type == BankTransactionModel.CAPITAL:
                bank.capital += instance.amount

            if instance.transaction_type == BankTransactionModel.LOAN:
                bank.loan += instance.amount

            bank.save()
