from finsys.models import FixedAssetsModel, BankModel, BankTransactionModel, FixedAssetsHistoryModel


class FixedAssetsSignal:

    @classmethod
    def post_change_balance(cls, sender, instance, created, **kwargs):
        fixed_asset = FixedAssetsModel.objects.all().first()
        bank = BankModel.objects.filter(pk=instance.bank.pk).first()

        if fixed_asset and bank:
            fixed_asset.balance += instance.amount
            fixed_asset.save()

        if created:
            BankTransactionModel.objects.create(
                date=instance.date,
                user=instance.user,
                bank=instance.bank,
                head="Fixed Asset",
                from_where=instance.from_where,
                transaction_type=BankTransactionModel.DEBIT,
                amount=instance.amount,
                foreign_id=instance.id,
            )
        else:
            if not instance.is_deleted:
                transaction = BankTransactionModel.objects.filter(foreign_id=instance.id, head="Fixed Asset").first()
                transaction.amount = instance.amount
                transaction.save()

    @classmethod
    def pre_change_balance(cls, sender, instance, **kwargs):
        fixed_asset = FixedAssetsModel.objects.all().first()
        history = FixedAssetsHistoryModel.objects.filter(pk=instance.pk).first()
        bank = BankModel.objects.filter(pk=instance.bank.pk).first()

        if not fixed_asset or not history or not bank:
            return

        fixed_asset.balance -= history.amount
        fixed_asset.save()

        bank.balance -= history.amount
        bank.save()
