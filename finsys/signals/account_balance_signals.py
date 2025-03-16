from finsys.models import AccountModel, BankTransactionModel, AccountHistoryModel, BankModel


class AccountBalanceSignals:

    @classmethod
    def post_change_balance(cls, sender, instance, created, **kwargs):
        account = AccountModel.objects.filter(pk=instance.account.pk).first()
        bank = BankModel.objects.filter(pk=instance.bank.pk).first()
        if account and bank:
            account.balance += instance.amount
            account.save()

        if created:
            transaction_type = BankTransactionModel.CREDIT if instance.account.account_type == BankTransactionModel.CREDIT else BankTransactionModel.DEBIT
            BankTransactionModel.objects.create(
                date=instance.date,
                user=instance.user,
                bank=instance.bank,
                head=instance.account.name,
                from_where=instance.from_where,
                transaction_type=transaction_type,
                amount=instance.amount,
                foreign_id=instance.id,
            )
        else:
            transaction = BankTransactionModel.objects.filter(foreign_id=instance.id).first()
            transaction.amount = instance.amount
            transaction.save()

    @classmethod
    def pre_change_balance(cls, sender, instance, **kwargs):
        account = AccountModel.objects.filter(pk=instance.account.pk).first()
        history = AccountHistoryModel.objects.filter(pk=instance.pk).first()
        bank = BankModel.objects.filter(pk=instance.bank.pk).first()

        if not account or not history or not bank:
            return

        account.balance -= history.amount
        account.save()

        transaction_type = BankTransactionModel.DEBIT if instance.account.account_type == BankTransactionModel.CREDIT else BankTransactionModel.CREDIT
        BankTransactionModel.objects.create(
            date=instance.date,
            user=instance.user,
            bank=instance.bank,
            head=instance.account.name,
            from_where=instance.from_where,
            transaction_type=transaction_type,
            amount=history.amount,
            is_deleted=True
        )
