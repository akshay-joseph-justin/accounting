from finsys.models import FixedAssetsHistoryModel, CapitalHistoryModel


class DepreciationSignals:

    @classmethod
    def post_change_total(cls, sender, instance, created, **kwargs):
        if created:
            asset = FixedAssetsHistoryModel.objects.get(pk=instance.asset.pk)
            asset.depreciation += instance.amount
            asset.save()

            entries = CapitalHistoryModel.objects.all()
            count = entries.count()
            for entry in entries:
                entry.amount -= instance.amount / count
                entry.save()
