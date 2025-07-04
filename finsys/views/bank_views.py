from django.db.models import Q
from django.urls import reverse_lazy
from django.views import generic

from finsys import models
from finsys.forms import BankUpsertForm, BankDepositForm, BankTransferForm
from finsys.models import BankTransactionModel, BankModel
from finsys.views.delete import DeleteView


class BankView(generic.ListView):
    context_object_name = 'banks'
    template_name = "finsys/wallet.html"

    def get_queryset(self):
        return BankModel.objects.filter(company_id=self.request.session["CURRENT_COMPANY_ID"])


class BankDetailView(generic.DetailView):
    model = models.BankModel
    context_object_name = 'bank'
    template_name = "finsys/bank-details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["transactions"] = models.BankTransactionModel.objects.filter(bank=self.object, is_deleted=False,
                                                                             year__year__exact=self.request.session[
                                                                                 "CURRENT_YEAR"])
        return context


class BankCreateView(generic.CreateView):
    model = models.BankModel
    form_class = BankUpsertForm
    template_name = "finsys/bank-create.html"
    success_url = reverse_lazy('finsys:wallet')

    def form_valid(self, form):
        form.instance.company_id = self.request.session["CURRENT_COMPANY_ID"]
        return super().form_valid(form)


class BankUpdateView(generic.UpdateView):
    model = models.BankModel
    form_class = BankUpsertForm
    template_name = "finsys/bank-create.html"
    success_url = reverse_lazy('finsys:wallet')


class BankDeleteView(generic.DeleteView):
    model = models.BankModel
    success_url = reverse_lazy('finsys:wallet')

    def get(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class BankAddAmountView(generic.TemplateView, generic.FormView):
    model = models.BankTransactionModel
    form_class = BankDepositForm
    template_name = "finsys/bank-add-amount.html"
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
            year_id=self.request.session["CURRENT_YEAR_ID"],
        )

        return super().form_valid(form)


class BankTransactionDeleteView(DeleteView):
    model = BankTransactionModel

    def get_success_url(self):
        return reverse_lazy('finsys:bank-details', kwargs={'pk': self.kwargs['bank_pk']})

    def get(self, request, *args, **kwargs):
        bank = BankModel.objects.filter(pk=kwargs['bank_pk']).first()
        entry = BankTransactionModel.objects.filter(pk=kwargs['pk']).first()
        bank.balance -= entry.amount
        bank.save()
        BankTransactionModel.objects.filter(pk=kwargs['pk']).update(is_deleted=True)

        return super().get(request, *args, **kwargs)


class BankTransferView(generic.TemplateView, generic.FormView):
    form_class = BankTransferForm
    template_name = "finsys/account-transaction.html"
    success_url = reverse_lazy('finsys:bank-transfer')

    def form_valid(self, form):
        debit = models.BankTransactionModel.objects.create(
            user=self.request.user,
            bank=form.cleaned_data['from_where'],
            date=form.cleaned_data['date'],
            head=form.cleaned_data['from_where'],
            from_where=form.cleaned_data['to'],
            transaction_type=models.BankTransactionModel.DEBIT,
            amount=form.cleaned_data['amount'],
            year_id=self.request.session["CURRENT_YEAR_ID"]
        )
        models.BankTransactionModel.objects.create(
            user=self.request.user,
            bank=form.cleaned_data['to'],
            date=form.cleaned_data['date'],
            head=form.cleaned_data['to'],
            from_where=form.cleaned_data['from_where'],
            transaction_type=models.BankTransactionModel.CREDIT,
            amount=form.cleaned_data['amount'],
            foreign_id=debit.id,
            year_id=self.request.session["CURRENT_YEAR_ID"]
        )

        return super().form_valid(form)


class BankTransferListView(generic.ListView):
    model = models.BankTransactionModel
    context_object_name = 'transactions'
    template_name = "finsys/bank-transfer.html"

    def get_queryset(self):
        bank_names = models.BankModel.objects.filter(company_id=self.request.session["CURRENT_COMPANY_ID"]).values_list(
            'name', flat=True)  # List of bank names

        # Build Q object dynamically for filtering 'from_where'
        q_object = Q()
        for bank_name in bank_names:
            q_object |= Q(from_where__icontains=bank_name)  # Case-insensitive match

        return models.BankTransactionModel.objects.filter(q_object, transaction_type=BankTransactionModel.CREDIT,
                                                          is_deleted=False,
                                                          year_id=self.request.session["CURRENT_YEAR_ID"])


class BankTransferDeleteView(DeleteView):
    model = BankTransactionModel
    success_url = reverse_lazy("finsys:bank-transfer")

    def change_balance(self, entry):
        bank = models.BankModel.objects.get(pk=entry.bank.pk)
        if entry.transaction_type == models.BankTransactionModel.CREDIT:
            bank.balance -= entry.amount
        if entry.transaction_type == models.BankTransactionModel.DEBIT:
            bank.balance += entry.amount
        bank.save()

    def get(self, request, *args, **kwargs):
        entry = BankTransactionModel.objects.filter(pk=kwargs['pk']).first()
        entry2 = BankTransactionModel.objects.filter(pk=entry.foreign_id).first()
        self.change_balance(entry)
        self.change_balance(entry2)
        BankTransactionModel.objects.filter(id=entry.id).update(is_deleted=True)
        BankTransactionModel.objects.filter(id=entry2.id).update(is_deleted=True)

        return super().get(request, *args, **kwargs)
