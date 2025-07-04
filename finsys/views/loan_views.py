from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, ListView, DetailView, FormView

from finsys.forms import LoanForm, LoanPayForm
from finsys.models import LoanModel, LoanHistoryModel, BankTransactionModel, BankModel
from finsys.views.delete import DeleteView


class LoanView(TemplateView):
    template_name = "finsys/loan.html"

    def get_context_data(self, **kwargs):
        loan = LoanModel.objects.filter(company_id=self.request.session["CURRENT_COMPANY_ID"],
                                        year_id=self.request.session["CURRENT_YEAR_ID"]).first()
        entries = LoanHistoryModel.objects.filter(is_deleted=False, amount__gt=0,
                                                  company=self.request.session["CURRENT_COMPANY_ID"],
                                                  year_id=self.request.session["CURRENT_YEAR_ID"])
        return {"loan": loan, "entries": entries}


class LoanDetailView(DetailView):
    template_name = "finsys/capital-details.html"
    context_object_name = "ledger"

    def get_queryset(self):
        return LoanHistoryModel.objects.filter(is_deleted=False, year_id=self.request.session["CURRENT_YEAR_ID"],
                                               company_id=self.request.session["CURRENT_COMPANY_ID"])


class LoanCreateView(CreateView):
    model = LoanHistoryModel
    template_name = "finsys/add-loan.html"
    form_class = LoanForm
    success_url = reverse_lazy("finsys:loan")

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.company_id = self.request.session["CURRENT_COMPANY_ID"]
        form.instance.year_id = self.request.session["CURRENT_YEAR_ID"]
        return super().form_valid(form)


class LoanUpdateView(UpdateView):
    model = LoanHistoryModel
    template_name = "finsys/add-loan.html"
    form_class = LoanForm
    success_url = reverse_lazy("finsys:loan")


class LoanDeleteView(DeleteView):
    model = LoanHistoryModel
    success_url = reverse_lazy("finsys:loan")

    def get(self, request, *args, **kwargs):
        loan = LoanModel.objects.filter(company_id=self.request.session["CURRENT_COMPANY_ID"],
                                        year_id=self.request.session["CURRENT_YEAR_ID"]).first()
        entry = LoanHistoryModel.objects.filter(pk=kwargs['pk']).first()
        loan.balance -= entry.amount
        loan.save()
        BankTransactionModel.objects.filter(foreign_id=entry.id, head__iexact="Loan").update(is_deleted=True)

        return super().get(request, *args, **kwargs)


class LoanHistoryView(ListView):
    template_name = "finsys/history.html"
    context_object_name = 'entries'
    ordering = ['-date']

    def get_queryset(self):
        instance = LoanHistoryModel.objects.get(pk=self.kwargs['pk'],
                                                company=self.request.session["CURRENT_COMPANY_ID"],
                                                year_id=self.request.session["CURRENT_YEAR_ID"])
        if instance:
            return instance.history.all()
        return LoanHistoryModel.objects.none()


class LoanPayView(TemplateView, FormView):
    template_name = "finsys/loan-pay.html"
    form_class = LoanPayForm
    success_url = reverse_lazy("finsys:loan")

    def debit_amount_from_bank(self, amount, date, from_where):
        BankTransactionModel.objects.create(
            user=self.request.user,
            bank=BankModel.objects.get(pk=self.kwargs['bank_pk']),
            date=date,
            head="Loan",
            from_where=from_where,
            transaction_type=BankTransactionModel.DEBIT,
            amount=amount,
            year_id=self.request.session["CURRENT_YEAR_ID"]
        )

    def form_valid(self, form):
        self.debit_amount_from_bank(form.cleaned_data["principle_amount"], form.cleaned_data["date"], "Principle Loan")
        self.debit_amount_from_bank(form.cleaned_data["interest"], form.cleaned_data["date"], "Loan Interest")

        loan = LoanHistoryModel.objects.get(pk=self.kwargs['history_pk'],
                                            company=self.request.session["CURRENT_COMPANY_ID"])
        loan.amount -= form.cleaned_data["principle_amount"]
        loan.save()
        LoanHistoryModel.objects.create(
            company_id=self.request.session["CURRENT_COMPANY_ID"],
            user=self.request.user,
            bank=BankModel.objects.get(pk=self.kwargs['bank_pk']),
            date=form.cleaned_data["date"],
            from_where=form.cleaned_data["from_where"],
            amount=-form.cleaned_data["principle_amount"],
            pending_amount=loan.amount,
            is_pay=True,
            year_id=self.request.session["CURRENT_YEAR_ID"]
        )

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["entries"] = LoanHistoryModel.objects.filter(is_deleted=False, amount__lt=0,
                                                             company=self.request.session["CURRENT_COMPANY_ID"],
                                                             year_id=self.request.session["CURRENT_YEAR_ID"])
        return context
