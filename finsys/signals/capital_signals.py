from finsys.models import CapitalModel, CapitalHistoryModel, BankModel, BankTransactionModel


class CapitalSignal:

    @classmethod
    def post_change_balance(cls, sender, instance, created, **kwargs):
        capital = CapitalModel.objects.all().first()
        bank = BankModel.objects.filter(pk=instance.bank.pk).first()
        if capital and bank:
            capital.balance += instance.amount
            capital.save()

        if created:
            BankTransactionModel.objects.create(
                date=instance.date,
                user=instance.user,
                bank=instance.bank,
                head="Capital",
                from_where=instance.from_where,
                transaction_type=BankTransactionModel.CREDIT,
                amount=instance.amount,
                foreign_id=instance.id,
            )
        else:
            if not instance.is_deleted:
                transaction = BankTransactionModel.objects.filter(foreign_id=instance.id, head="Capital").first()
                transaction.amount = instance.amount
                transaction.save()

    @classmethod
    def pre_change_balance(cls, sender, instance, **kwargs):
        capital = CapitalModel.objects.all().first()
        history = CapitalHistoryModel.objects.filter(pk=instance.pk).first()
        bank = BankModel.objects.filter(pk=instance.bank.pk).first()

        if not capital or not history or not bank:
            return

        capital.balance -= history.amount
        capital.save()

        bank.balance -= history.amount
        bank.save()
