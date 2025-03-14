from finsys.models import CapitalModel, CapitalHistoryModel, BankModel, BankTransactionModel


class CapitalSignal:

    @classmethod
    def post_change_balance(cls, sender, instance, created, **kwargs):
        capital = CapitalModel.objects.filter(pk=1).first()
        bank = BankModel.objects.filter(pk=instance.bank.pk).first()
        if capital and bank:
            capital.balance += instance.amount
            capital.save()

            BankTransactionModel.objects.create(
                user=instance.user,
                date=instance.date,
                bank=instance.bank,
                head="Capital",
                from_where=instance.from_where,
                transaction_type=BankTransactionModel.CREDIT,
                amount=instance.amount
            )

    @classmethod
    def pre_change_balance(cls, sender, instance, **kwargs):
        capital = CapitalModel.objects.filter(pk=1).first()
        history = CapitalHistoryModel.objects.filter(pk=instance.pk).first()
        bank = BankModel.objects.filter(pk=instance.bank.pk).first()
        if not capital:
            return
        if not history:
            return
        if not bank:
            return

        capital.balance -= history.amount
        capital.save()

        BankTransactionModel.objects.create(
            user=instance.user,
            date=instance.date,
            bank=instance.bank,
            head="Capital",
            from_where=instance.from_where,
            transaction_type=BankTransactionModel.DEBIT,
            amount=history.amount
        )
