from django.urls import reverse_lazy
from django.views import generic

from finsys import generate_random_number
from finsys.forms import BankUpsertForm, BankDepositForm
from finsys import models


class BankView(generic.ListView):
    model = models.BankModel
    context_object_name = 'banks'
    template_name = "wallet.html"


class BankDetailView(generic.DetailView):
    model = models.BankModel
    context_object_name = 'bank'
    template_name = "bank-details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["transactions"] = models.BankTransactionModel.objects.filter(bank=self.object, is_deleted=False)
        return context


class BankCreateView(generic.CreateView):
    model = models.BankModel
    form_class = BankUpsertForm
    template_name = "bank-create.html"
    success_url = reverse_lazy('finsys:wallet')


class BankUpdateView(generic.UpdateView):
    model = models.BankModel
    form_class = BankUpsertForm
    template_name = "bank-create.html"
    success_url = reverse_lazy('finsys:wallet')


class BankAddAmountView(generic.TemplateView, generic.FormView):
    model = models.BankTransactionModel
    form_class = BankDepositForm
    template_name = "bank-add-amount.html"
    success_url = reverse_lazy('finsys:wallet')

    def form_valid(self, form):
        bank = models.BankModel.objects.get(pk=self.kwargs['pk'])
        transaction = self.model.objects.create(
            user=self.request.user,
            bank=bank,
            date=form.cleaned_data['date'],
            from_where=form.cleaned_data['from_where'],
            transaction_type=self.model.CREDIT,
            amount=form.cleaned_data['amount'],
        )

        return super().form_valid(form)

