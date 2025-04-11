from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic.list import ListView

from finsys.forms import AccountForm, ReceiptForm
from finsys.models import AccountModel


class ReceiptView(ListView):
    model = AccountModel
    context_object_name = 'accounts'
    template_name = 'receipt.html'

    def get_queryset(self):
        return AccountModel.objects.filter(account_type=AccountModel.CREDIT)


class ReceiptCreateView(CreateView):
    model = AccountModel
    form_class = ReceiptForm
    template_name = "add-receipt.html"
    success_url = reverse_lazy("finsys:receipt")

    def form_valid(self, form):
        form.instance.account_type = AccountModel.CREDIT
        return super().form_valid(form)


class PaymentView(ListView):
    model = AccountModel
    context_object_name = 'accounts'
    template_name = 'payment.html'

    def get_queryset(self):
        return AccountModel.objects.filter(account_type=AccountModel.DEBIT)


class PaymentCreateView(CreateView):
    model = AccountModel
    form_class = ReceiptForm
    template_name = "add-payment.html"
    success_url = reverse_lazy("finsys:payment")

    def form_valid(self, form):
        form.instance.account_type = AccountModel.DEBIT
        return super().form_valid(form)

