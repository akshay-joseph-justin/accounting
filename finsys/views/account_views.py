from django.urls import reverse_lazy
from django.views import generic

from finsys.forms import AccountForm, AccountHistoryForm
from finsys.models import AccountModel, AccountHistoryModel, BankTransactionModel
from finsys.views.delete import DeleteView
from users.models import CompanyModel

class AccountListView(generic.ListView):
    context_object_name = 'accounts'
    ordering = ['name']
    template_name = "finsys/ledger.html"

    def get_queryset(self):
        return AccountModel.objects.filter(company_id=self.request.session["CURRENT_COMPANY_ID"])


class AccountDetailView(generic.DetailView):
    context_object_name = 'account'
    template_name = "finsys/ledger-details.html"

    def get_queryset(self):
        return AccountModel.objects.filter(company_id=self.request.session["CURRENT_COMPANY_ID"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["entries"] = AccountHistoryModel.objects.filter(account=self.object, is_deleted=False)
        return context


class AccountCreateView(generic.CreateView):
    form_class = AccountForm
    model = AccountModel
    template_name = "finsys/add-ledger.html"
    success_url = reverse_lazy("finsys:ledger")

    def get_initial(self):
        return {
            "company": self.request.session["CURRENT_COMPANY_ID"],
        }


class AccountUpdateView(generic.UpdateView):
    form_class = AccountForm
    model = AccountModel
    template_name = "finsys/add-ledger.html"
    success_url = reverse_lazy("finsys:account-list")


class AccountDeleteView(generic.DeleteView):
    model = AccountModel
    success_url = reverse_lazy("finsys:ledger")

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


class AccountHistoryCreateView(generic.CreateView):
    model = AccountHistoryModel
    form_class = AccountHistoryForm
    template_name = "finsys/account-transaction.html"

    def form_valid(self, form):
        account = AccountModel.objects.get(pk=self.kwargs['pk'])
        company = CompanyModel.objects.get(pk=self.request.session["CURRENT_COMPANY_ID"])
        form.instance.user = self.request.user
        form.instance.account = account
        form.instance.from_where = account.name
        form.instance.company = company
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("finsys:ledger-details", kwargs={"pk": self.kwargs['pk']})


class AccountHistoryUpdateView(generic.UpdateView):
    model = AccountHistoryModel
    form_class = AccountHistoryForm
    template_name = "finsys/account-transaction.html"

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
    template_name = "finsys/history.html"
    context_object_name = 'entries'
    ordering = ['-date']

    def get_queryset(self):
        instance = AccountHistoryModel.objects.get(pk=self.kwargs['pk'])
        if instance:
            return instance.history.all()
        return AccountHistoryModel.objects.none()
