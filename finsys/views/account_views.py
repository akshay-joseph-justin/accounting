from django.urls import reverse_lazy
from django.views import generic

from finsys.forms import AccountForm, AccountHistoryForm
from finsys.models import AccountModel, AccountHistoryModel, BankTransactionModel
from finsys.views.delete import DeleteView


class AccountListView(generic.ListView):
    model = AccountModel
    context_object_name = 'accounts'
    ordering = ['name']
    template_name = "ledger.html"


class AccountDetailView(generic.DetailView):
    model = AccountModel
    context_object_name = 'account'
    template_name = "ledger-details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["entries"] = AccountHistoryModel.objects.filter(account=self.object, is_deleted=False)
        return context


class AccountCreateView(generic.CreateView):
    form_class = AccountForm
    model = AccountModel
    template_name = "add-ledger.html"
    success_url = reverse_lazy("finsys:ledger")


class AccountUpdateView(generic.UpdateView):
    form_class = AccountForm
    model = AccountModel
    template_name = "add-ledger.html"
    success_url = reverse_lazy("finsys:account-list")


class AccountDeleteView(generic.DeleteView):
    model = AccountModel
    success_url = reverse_lazy("finsys:ledger")

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


class AccountHistoryCreateView(generic.CreateView):
    model = AccountHistoryModel
    form_class = AccountHistoryForm
    template_name = "account-transaction.html"

    def form_valid(self, form):
        account = AccountModel.objects.get(pk=self.kwargs['pk'])
        form.instance.user = self.request.user
        form.instance.account = account
        form.instance.from_where = account.name
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("finsys:ledger-details", kwargs={"pk": self.kwargs['pk']})


class AccountHistoryUpdateView(generic.UpdateView):
    model = AccountHistoryModel
    form_class = AccountHistoryForm
    template_name = "account-transaction.html"

    def get_success_url(self):
        return reverse_lazy("finsys:ledger-details", kwargs={"pk": self.kwargs['pk']})


class AccountHistoryDeleteView(DeleteView):
    model = AccountHistoryModel

    def get_success_url(self):
        return reverse_lazy("finsys:ledger-details", kwargs={"pk": self.kwargs['pk']})

    def get(self, request, *args, **kwargs):
        account = AccountModel.objects.filter(pk=kwargs['acc_pk']).first()
        entry = AccountHistoryModel.objects.filter(pk=kwargs['pk']).first()
        account.balance -= entry.amount
        account.save()
        BankTransactionModel.objects.filter(foreign_id=entry.id, head=account.name).update(is_deleted=True)

        return super().get(request, *args, **kwargs)


class AccountHistoryView(generic.ListView):
    template_name = "history.html"
    context_object_name = 'entries'
    ordering = ['-date']

    def get_queryset(self):
        instance = AccountHistoryModel.objects.get(pk=self.kwargs['pk'])
        if instance:
            return instance.history.all()
        return AccountHistoryModel.objects.none()
