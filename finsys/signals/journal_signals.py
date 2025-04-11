from finsys.models import JournalModel, BankModel, BankTransactionModel


class JournalSignal:

    @classmethod
    def post_change_balance(cls, sender, instance, created, **kwargs):
        if not instance.bank or instance.bank is None:
            return

        if created:
            BankTransactionModel.objects.create(
                date=instance.date,
                user=instance.user,
                bank=instance.bank,
                head="Journal",
                from_where=instance.from_where,
                transaction_type=instance.transaction_type,
                amount=instance.amount,
                foreign_id=instance.id,
            )
        else:
            if not instance.is_deleted:
                transaction = BankTransactionModel.objects.filter(foreign_id=instance.id, head="Journal").first()
                transaction.amount = instance.amount
                transaction.save()

    @classmethod
    def pre_change_balance(cls, sender, instance, **kwargs):
        if not instance.bank or instance.bank is None:
            return

        history = JournalModel.objects.filter(pk=instance.pk).first()
        bank = BankModel.objects.filter(pk=instance.bank.pk).first()

        if not history:
            return

        bank.balance -= history.amount
        bank.save()


