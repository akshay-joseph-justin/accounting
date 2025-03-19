from django.db.models import Q
from django.urls import reverse_lazy
from django.views import generic

from finsys import models
from finsys.forms import BankUpsertForm, BankDepositForm, BankTransferForm


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


class BankTransferView(generic.TemplateView, generic.FormView):
    form_class = BankTransferForm
    template_name = "add-ledger.html"
    success_url = reverse_lazy('finsys:bank-transfer')

    def form_valid(self, form):
        models.BankTransactionModel.objects.create(
            user=self.request.user,
            bank=form.cleaned_data['to'],
            date=form.cleaned_data['date'],
            head=form.cleaned_data['to'],
            from_where=form.cleaned_data['from_where'],
            transaction_type=models.BankTransactionModel.CREDIT,
            amount=form.cleaned_data['amount'],
        )

        models.BankTransactionModel.objects.create(
            user=self.request.user,
            bank=form.cleaned_data['from_where'],
            date=form.cleaned_data['date'],
            head=form.cleaned_data['from_where'],
            from_where=form.cleaned_data['to'],
            transaction_type=models.BankTransactionModel.DEBIT,
            amount=form.cleaned_data['amount'],
        )

        return super().form_valid(form)


class BankTransferListView(generic.ListView):
    model = models.BankTransactionModel
    context_object_name = 'transactions'
    template_name = "bank-transfer.html"

    def get_queryset(self):
        bank_names = models.BankModel.objects.values_list('name', flat=True)  # List of bank names

        # Build Q object dynamically for filtering 'from_where'
        q_object = Q()
        for bank_name in bank_names:
            q_object |= Q(from_where__icontains=bank_name)  # Case-insensitive match

        return models.BankTransactionModel.objects.filter(q_object)
