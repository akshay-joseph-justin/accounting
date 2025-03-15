from finsys.models import FixedAssetsModel, FixedAssetsHistoryModel, BankModel, BankTransactionModel


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
