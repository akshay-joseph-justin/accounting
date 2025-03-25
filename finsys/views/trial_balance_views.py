from django.views.generic import ListView

from finsys.models import BankTransactionModel

class TrialBalanceView(ListView):
    model = BankTransactionModel
    context_object_name = 'transactions'
    template_name = 'trial-balance.html'
