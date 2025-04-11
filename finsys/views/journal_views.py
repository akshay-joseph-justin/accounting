from django.db.models import F
from django.urls import reverse_lazy
from django.views import generic

from finsys.forms import JournalForm
from finsys.models import JournalModel, BankTransactionModel, BankModel, DepreciationModel
from finsys.views.delete import DeleteView


class JournalListView(generic.ListView):
    context_object_name = 'entries'
    template_name = 'journal.html'

    def get_queryset(self):
        return JournalModel.objects.filter(is_deleted=False)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["depreciations"] = DepreciationModel.objects.all()
        return data


class JournalDetailView(generic.DetailView):
    pass


class JournalCreateView(generic.CreateView):
    model = JournalModel
    form_class = JournalForm
    template_name = 'account-transaction.html'
    success_url = reverse_lazy('finsys:journal')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class JournalUpdateView(generic.UpdateView):
    model = JournalModel
    form_class = JournalForm
    template_name = 'account-transaction.html'
    success_url = reverse_lazy('finsys:journal')


class JournalDeleteView(DeleteView):
    model = JournalModel
    success_url = reverse_lazy("finsys:journal")

    def get(self, request, *args, **kwargs):
        entry = JournalModel.objects.filter(pk=kwargs['pk']).first()
        if entry.transaction_type == JournalModel.CREDIT:
            BankModel.objects.filter(pk=entry.bank.pk).update(balance=F("balance") - entry.amount)
        if entry.transaction_type == JournalModel.DEBIT:
            BankModel.objects.filter(pk=entry.bank.pk).update(balance=F("balance") + entry.amount)
        BankTransactionModel.objects.filter(foreign_id=entry.id, head__iexact="Journal").update(is_deleted=True)

        return super().get(request, *args, **kwargs)
