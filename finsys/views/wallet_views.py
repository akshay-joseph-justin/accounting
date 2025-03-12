from django.urls import reverse_lazy
from django.views import generic

from finsys.forms import AccountForm, BankForm
from finsys.models import AccountModel
from finsys import generate_random_number


class BankView(generic.ListView):
    queryset = AccountModel.objects.filter(is_bank=True)
    context_object_name = 'banks'
    template_name = "wallet.html"


class BankCreateView(generic.CreateView):
    model = AccountModel
    form_class = BankForm
    template_name = "bank-create.html"
    success_url = reverse_lazy('finsys:wallet')

    def form_valid(self, form):
        form.instance.code = generate_random_number(4)
        form.instance.account_type = AccountModel.CREDIT
        form.instance.is_bank = True
        return super(BankCreateView, self).form_valid(form)
