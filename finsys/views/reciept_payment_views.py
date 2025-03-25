from django.views.generic.list import ListView

from finsys.models import AccountModel


class ReceiptView(ListView):
    model = AccountModel
    context_object_name = 'accounts'
    template_name = 'receipt.html'

    def get_queryset(self):
        return AccountModel.objects.filter(account_type=AccountModel.CREDIT)


class PaymentView(ListView):
    model = AccountModel
    context_object_name = 'accounts'
    template_name = 'payment.html'

    def get_queryset(self):
        return AccountModel.objects.filter(account_type=AccountModel.DEBIT)
