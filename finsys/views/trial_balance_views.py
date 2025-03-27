from django.db.models import Sum
from django.views.generic import ListView

from finsys.models import BankTransactionModel, BankModel

class TrialBalanceView(ListView):
    model = BankTransactionModel
    context_object_name = 'transactions'
    template_name = 'trial-balance.html'

    def get_context_data(self, **kwargs):
        context = super(TrialBalanceView, self).get_context_data(**kwargs)
        context["total"] = BankModel.objects.aggregate(total=Sum("balance"))["total"]
        context["banks"] = BankModel.objects.all()
        return context
