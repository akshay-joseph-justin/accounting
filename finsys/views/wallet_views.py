from django.urls import reverse_lazy
from django.views import generic

from finsys import generate_random_number
from finsys.forms import BankUpsertForm, BankDepositForm
from finsys.models import AccountModel, JournalEntryModel, JournalEntryLineModel


class BankView(generic.ListView):
    queryset = AccountModel.objects.filter(is_bank=True)
    context_object_name = 'banks'
    template_name = "wallet.html"


class BankDetailView(generic.DetailView):
    model = AccountModel
    context_object_name = 'bank'
    template_name = "bank-details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["entries"] = JournalEntryModel.objects.filter(lines__account=self.object)
        return context


class BankCreateView(generic.CreateView):
    model = AccountModel
    form_class = BankUpsertForm
    template_name = "bank-create.html"
    success_url = reverse_lazy('finsys:wallet')

    def form_valid(self, form):
        form.instance.code = generate_random_number(4)
        form.instance.account_type = AccountModel.CREDIT
        form.instance.is_bank = True
        return super(BankCreateView, self).form_valid(form)


class BankAddAmountView(generic.TemplateView, generic.FormView):
    form_class = BankDepositForm
    template_name = "bank-add-amount.html"

    def form_valid(self, form):
        bank = AccountModel.objects.filter(id=self.kwargs.get('pk'), is_bank=True).first()
        if not bank:
            form.add_error(None, "Bank account not found.")
            return self.form_invalid(form)

        journal_entry = JournalEntryModel.objects.create(
            date=form.cleaned_data['date'],
            reference_number=generate_random_number(6),
            created_by=self.request.user
        )
        JournalEntryLineModel.objects.create(
            entry=journal_entry,
            account=bank,
            entry_type=JournalEntryLineModel.CREDIT,
            amount=form.cleaned_data['amount']
        )

        self.bank = bank  # Store bank instance for later use
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('finsys:bank-details', kwargs={'pk': self.kwargs.get('pk')})
