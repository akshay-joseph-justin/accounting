from django.urls import reverse_lazy
from django.views import generic

from finsys.forms import BankForm, BankTransactionForm
from finsys.models import BanKModel, BankTransactionModel


class WalletView(generic.ListView):
    model = BanKModel
    context_object_name = 'banks'
    template_name = 'wallet.html'


class BankDetailView(generic.DetailView):
    model = BanKModel
    context_object_name = 'bank'
    template_name = 'bank-details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["transactions"] = BankTransactionModel.objects.filter(bank=self.object).order_by('date')
        return context


class BankCreateView(generic.CreateView):
    model = BanKModel
    form_class = BankForm
    template_name = "bank-create.html"
    success_url = reverse_lazy('finsys:wallet')


class BankTransactionCreateView(generic.CreateView):
    model = BankTransactionModel
    form_class = BankTransactionForm
    template_name = "bank-transaction-create.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('finsys:bank-details', kwargs={'pk': self.object.bank.pk})