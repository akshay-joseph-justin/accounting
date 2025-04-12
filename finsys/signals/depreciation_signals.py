from django.db.models import F

from finsys.models import FixedAssetsHistoryModel, CapitalHistoryModel, CapitalModel, FixedAssetsModel


class DepreciationSignals:

    @classmethod
    def post_change_total(cls, sender, instance, created, **kwargs):
        if created:
            FixedAssetsHistoryModel.objects.filter(pk=instance.asset.pk).update(
                current_balance=F("current_balance") - instance.amount)

            FixedAssetsModel.objects.filter(pk=FixedAssetsModel.objects.first().pk).update(
                balance=F("balance") - instance.amount)

            CapitalModel.objects.filter(pk=CapitalModel.objects.first().pk).update(
                balance=F("balance") - instance.amount)

            entries = CapitalHistoryModel.objects.all()
            count = entries.count()
            for entry in entries:
                CapitalHistoryModel.objects.filter(pk=entry.pk).update(amount=F("amount") - (instance.amount / count))
