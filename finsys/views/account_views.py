from django.urls import reverse_lazy
from django.views import generic

from finsys.forms import AccountForm
from finsys.models import AccountModel, JournalEntryLineModel
from finsys.views.delete import DeleteView


class AccountListView(generic.ListView):
    model = AccountModel
    context_object_name = 'accounts'
    ordering = ['name']
    template_name = "ledger.html"

    def get_queryset(self):
        return self.model.objects.filter(is_inbuilt=False, is_bank=False)


class AccountDetailView(generic.DetailView):
    model = AccountModel
    context_object_name = 'account'
    template_name = ""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["entries"] = JournalEntryLineModel.objects.filter(account=self.object)
        return context


class AccountCreateView(generic.CreateView):
    form_class = AccountForm
    model = AccountModel
    template_name = "add-ledger.html"
    success_url = reverse_lazy("finsys:account-list")


class AccountUpdateView(generic.UpdateView):
    form_class = AccountForm
    model = AccountModel
    template_name = "account_create.html"
    success_url = reverse_lazy("finsys:account-list")


class AccountDeleteView(DeleteView):
    model = AccountModel
    success_url = reverse_lazy("finsys:account-list")
