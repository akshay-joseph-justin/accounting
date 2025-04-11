from finsys.models import FixedAssetsHistoryModel, CapitalModel, CapitalHistoryModel, JournalModel


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
                entry.amount -= instance.amount/count

            entry = FixedAssetsHistoryModel.objects.get(pk=instance.asset.pk)

            JournalModel.objects.create(
                user=instance.user,
                date=instance.date,
                from_where=entry.from_where,
                amount=instance.amount,
                transaction_type=JournalModel.DEBIT
            )
