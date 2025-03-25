from finsys.models import JournalModel, BankModel, BankTransactionModel


class CapitalSignal:

    @classmethod
    def post_change_balance(cls, sender, instance, created, **kwargs):
        bank = BankModel.objects.filter(pk=instance.bank.pk).first()

        if created:
            BankTransactionModel.objects.create(
                date=instance.date,
                user=instance.user,
                bank=instance.bank,
                head="Journal",
                from_where=instance.from_where,
                transaction_type=BankTransactionModel.CREDIT,
                amount=instance.amount,
                foreign_id=instance.id,
            )
        else:
            transaction = BankTransactionModel.objects.filter(foreign_id=instance.id).first()
            transaction.amount = instance.amount
            transaction.save()

    @classmethod
    def pre_change_balance(cls, sender, instance, **kwargs):
        history = JournalModel.objects.filter(pk=instance.pk).first()

        if not history:
            return

        BankTransactionModel.objects.create(
            date=instance.date,
            user=instance.user,
            bank=instance.bank,
            head="Journal",
            from_where=instance.from_where,
            transaction_type=BankTransactionModel.DEBIT,
            amount=history.amount,
            is_deleted=True
        )
