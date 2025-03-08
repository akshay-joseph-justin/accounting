from django.urls import reverse_lazy
from django.views import generic

from finsys.forms import AccountForm
from finsys.models import AccountModel
from finsys.views.delete import DeleteView

class AccountListView(generic.ListView):
    model = AccountModel
    context_object_name = 'accounts'
    ordering = ['name']
    template_name = "account_list.html"


class AccountCreateView(generic.CreateView):
    form_class = AccountForm
    model = AccountModel
    template_name = "account_create.html"
    success_url = reverse_lazy("finsys:account-list")


class AccountUpdateView(generic.UpdateView):
    form_class = AccountForm
    model = AccountModel
    template_name = "account_create.html"
    success_url = reverse_lazy("finsys:account-list")


class AccountDeleteView(DeleteView):
    model = AccountModel
    success_url = reverse_lazy("finsys:account-list")
