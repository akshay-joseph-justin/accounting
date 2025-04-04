from finsys.models import FixedAssetsHistoryModel, JournalModel, CapitalModel


class DepreciationSignals:

    @classmethod
    def post_change_total(cls, sender, instance, created, **kwargs):
        if created:
            asset = FixedAssetsHistoryModel.objects.get(pk=instance.asset.pk)
            asset.depreciation += instance.amount
            asset.save()

            JournalModel.objects.create(
                date=instance.date,
                from_where=f"FixedAsset - {asset.serial_number}",
                bank=None,
                amount=instance.amount,
                transaction_type=JournalModel.DEBIT,
            )

            capital = CapitalModel.objects.first()
            capital.balance += instance.amount
            capital.save()
