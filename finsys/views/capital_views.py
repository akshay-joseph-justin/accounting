from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView

from finsys import generate_random_number
from finsys.forms.capital_forms import CapitalForm
from finsys.models import AccountModel, JournalEntryModel, JournalEntryLineModel


class CapitalView(TemplateView):
    template_name = "capital.html"

    def get_context_data(self, **kwargs):
        capital = AccountModel.objects.filter(name="Capital").first()
        entries = JournalEntryModel.objects.filter(lines__account=capital).order_by('-lines__entry__date')
        return {"capital": capital, "entries": entries}


class CapitalAddAmountView(TemplateView, FormView):
    template_name = "add-capital.html"
    form_class = CapitalForm
    success_url = reverse_lazy("finsys:capital")

    def form_valid(self, form):
        capital = AccountModel.objects.filter(name="Capital").first()
        bank = AccountModel.objects.filter(id=form.cleaned_data["bank"].id).first()
        journal_entry = JournalEntryModel.objects.create(
            date=form.cleaned_data["date"],
            reference_number=generate_random_number(6),
            created_by=self.request.user,
        )
        journal_entry_line_capital = JournalEntryLineModel.objects.create(
            entry=journal_entry,
            account=capital,
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
