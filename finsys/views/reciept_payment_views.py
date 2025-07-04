from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic.list import ListView

from finsys.forms import AccountForm, ReceiptForm
from finsys.models import AccountModel


class ReceiptView(ListView):
    model = AccountModel
    context_object_name = 'accounts'
    template_name = 'finsys/receipt.html'

    def get_queryset(self):
        return AccountModel.objects.filter(account_type=AccountModel.CREDIT, company=self.request.session["CURRENT_COMPANY_ID"])


class ReceiptCreateView(CreateView):
    model = AccountModel
    form_class = ReceiptForm
    template_name = "finsys/add-receipt.html"
    success_url = reverse_lazy("finsys:receipt")

    def form_valid(self, form):
        form.instance.account_type = AccountModel.CREDIT
        form.instance.company_id = self.request.session["CURRENT_COMPANY_ID"]
        return super().form_valid(form)


class PaymentView(ListView):
    model = AccountModel
    context_object_name = 'accounts'
    template_name = 'finsys/payment.html'

    def get_queryset(self):
        return AccountModel.objects.filter(account_type=AccountModel.DEBIT, company=self.request.session["CURRENT_COMPANY_ID"])


class PaymentCreateView(CreateView):
    model = AccountModel
    form_class = ReceiptForm
    template_name = "finsys/add-payment.html"
    success_url = reverse_lazy("finsys:payment")

    def form_valid(self, form):
        form.instance.account_type = AccountModel.DEBIT
        form.instance.company_id = self.request.session["CURRENT_COMPANY_ID"]
        return super().form_valid(form)

