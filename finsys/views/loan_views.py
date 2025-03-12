from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView

from finsys import generate_random_number
from finsys.forms import LoanForm
from finsys.models import AccountModel, JournalEntryLineModel, JournalEntryModel


class LoanView(TemplateView):
    template_name = "loan.html"

    def get_context_data(self, **kwargs):
        loan = AccountModel.objects.filter(name="Loan").first()
        entries = JournalEntryModel.objects.filter(lines__account=loan).order_by('-lines__entry__date')
        return {"loan": loan, "entries": entries}


class LoanAddAmountView(TemplateView, FormView):
    template_name = "add-capital.html"
    form_class = LoanForm
    success_url = reverse_lazy("finsys:capital")

    def form_valid(self, form):
        loan = AccountModel.objects.filter(name="Loan").first()
        bank = AccountModel.objects.filter(id=form.cleaned_data["bank"].id).first()
        journal_entry = JournalEntryModel.objects.create(
            date=form.cleaned_data["date"],
            reference_number=generate_random_number(6),
            created_by=self.request.user,
        )
        journal_entry_line_capital = JournalEntryLineModel.objects.create(
            entry=journal_entry,
            account=loan,
            entry_type=JournalEntryLineModel.CREDIT,
            amount=form.cleaned_data["amount"],
        )
        journal_entry_line_bank = JournalEntryLineModel.objects.create(
            entry=journal_entry,
            account=bank,
            entry_type=JournalEntryLineModel.CREDIT,
            amount=form.cleaned_data["amount"],
        )

        return super().form_valid(form)
