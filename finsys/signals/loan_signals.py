from finsys.models import LoanModel, LoanHistoryModel, BankModel, BankTransactionModel


class LoanSignal:

    @classmethod
    def post_change_balance(cls, sender, instance, created, **kwargs):
        loan = LoanModel.objects.all().first()
        bank = BankModel.objects.filter(pk=instance.bank.pk).first()
        if loan and bank and not instance.is_pay:
            loan.balance += instance.amount
            loan.save()

        if created and not instance.is_pay:
            BankTransactionModel.objects.create(
                date=instance.date,
                user=instance.user,
                bank=instance.bank,
                head="Loan",
                from_where=instance.from_where,
                transaction_type=BankTransactionModel.CREDIT,
                amount=instance.amount,
                foreign_id=instance.id,
            )
        else:
            transaction = BankTransactionModel.objects.filter(foreign_id=instance.id).first()
            if transaction:
                transaction.amount = instance.amount
                transaction.save()

    @classmethod
    def pre_change_balance(cls, sender, instance, **kwargs):
        loan = LoanModel.objects.all().first()
        history = LoanHistoryModel.objects.filter(pk=instance.pk).first()
        bank = BankModel.objects.filter(pk=instance.bank.pk).first()

        if not loan or not history or not bank:
            return

        loan.balance -= history.amount
        loan.save()

        BankTransactionModel.objects.create(
            date=instance.date,
            user=instance.user,
            bank=instance.bank,
            head="Loan",
            from_where=instance.from_where,
            transaction_type=BankTransactionModel.DEBIT,
            amount=history.amount,
            is_deleted=True
        )
