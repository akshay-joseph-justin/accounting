from django.db.models import F

from finsys.models import FixedAssetsHistoryModel, JournalModel


class DepreciationSignals:

    @classmethod
    def post_change_total(cls, sender, instance, created, **kwargs):
        if created:
            asset = FixedAssetsHistoryModel.objects.get(pk=instance.asset.pk)
            asset.depreciation = F('depreciation') + instance.amount

            JournalModel.objects.create(
                date=instance.date,
                from_where=f"FixedAsset - {asset.serial_number}",
                bank=None,
                amount=instance.amount,

            )
