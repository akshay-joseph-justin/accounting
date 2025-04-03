from django.db.models import Sum
from django.views.generic import ListView

from finsys.models import BankTransactionModel, BankModel

class TrialBalanceView(ListView):
    model = BankTransactionModel
    context_object_name = 'transactions'
    template_name = 'trial-balance.html'

    def profit_loss(self):
        total_debit = BankTransactionModel.objects.filter(transaction_type=BankTransactionModel.DEBIT).aggregate(total=Sum('amount'))["total"] or 0
        total_credit = BankTransactionModel.objects.filter(transaction_type=BankTransactionModel.CREDIT).aggregate(total=Sum('amount'))["total"] or 0
        amount = total_credit - total_debit
        if amount < 0:
            return amount, "Loss"
        elif amount > 0:
            return amount, "Profit"
        return amount, "Balanced"

    def get_context_data(self, **kwargs):
        context = super(TrialBalanceView, self).get_context_data(**kwargs)
        context["total"] = BankModel.objects.aggregate(total=Sum("balance"))["total"]
        context["banks"] = BankModel.objects.all()
        amount, status = self.profit_loss()
        context["amount"] = abs(amount)
        context["status"] = status
        return context
