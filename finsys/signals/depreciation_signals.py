from finsys.models import FixedAssetsHistoryModel, JournalModel, CapitalModel


class DepreciationSignals:

    @classmethod
    def post_change_total(cls, sender, instance, created, **kwargs):
        if created:
            asset = FixedAssetsHistoryModel.objects.get(pk=instance.asset.pk)
            asset.depreciation += instance.amount
            asset.save()

            capital = CapitalModel.objects.first()
            capital.balance -= instance.amount
            capital.save()
