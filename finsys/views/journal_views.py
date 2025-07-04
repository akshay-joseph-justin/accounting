from django.db.models import F
from django.urls import reverse_lazy
from django.views import generic

from finsys.forms import JournalForm
from finsys.models import JournalModel, BankTransactionModel, BankModel, DepreciationModel
from finsys.views.delete import DeleteView


class JournalListView(generic.ListView):
    context_object_name = 'entries'
    template_name = 'finsys/journal.html'

    def get_queryset(self):
        return JournalModel.objects.filter(is_deleted=False, company=self.request.session["CURRENT_COMPANY_ID"], year_id=self.request.session["CURRENT_YEAR_ID"])

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["depreciations"] = DepreciationModel.objects.filter(asset__bank__company_id=self.request.session["CURRENT_COMPANY_ID"], asset__year_id=self.request.session["CURRENT_YEAR_ID"])
        return data


class JournalDetailView(generic.DetailView):
    pass


class JournalCreateView(generic.CreateView):
    model = JournalModel
    form_class = JournalForm
    template_name = 'finsys/account-transaction.html'
    success_url = reverse_lazy('finsys:journal')

    def get_initial(self):
        return {"company": self.request.session["CURRENT_COMPANY_ID"]}

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.company_id = self.request.session["CURRENT_COMPANY_ID"]
        form.instance.year_id = self.request.session["CURRENT_YEAR_ID"]
        return super().form_valid(form)


class JournalUpdateView(generic.UpdateView):
    model = JournalModel
    form_class = JournalForm
    template_name = 'finsys/account-transaction.html'
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
