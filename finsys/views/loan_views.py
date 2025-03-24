from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, ListView, DetailView, FormView

from finsys.forms import LoanForm, LoanPayForm
from finsys.models import LoanModel, LoanHistoryModel, BankTransactionModel, BankModel


class LoanView(TemplateView):
    template_name = "loan.html"

    def get_context_data(self, **kwargs):
        loan = LoanModel.objects.all().first()
        entries = LoanHistoryModel.objects.filter(is_deleted=False, amount__gt=0)
        return {"loan": loan, "entries": entries}

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class LoanDetailView(DetailView):
    template_name = "capital-details.html"
    context_object_name = "ledger"

    def get_queryset(self):
        return LoanHistoryModel.objects.filter(is_deleted=False)


class LoanCreateView(CreateView):
    model = LoanHistoryModel
    template_name = "add-loan.html"
    form_class = LoanForm
    success_url = reverse_lazy("finsys:loan")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class LoanUpdateView(UpdateView):
    model = LoanHistoryModel
    template_name = "add-loan.html"
    form_class = LoanForm
    success_url = reverse_lazy("finsys:loan")


class LoanHistoryView(ListView):
    template_name = "history.html"
    context_object_name = 'entries'
    ordering = ['-date']

    def get_queryset(self):
        instance = LoanHistoryModel.objects.get(pk=self.kwargs['pk'])
        if instance:
            return instance.history.all()
        return LoanHistoryModel.objects.none()


class LoanPayView(TemplateView, FormView):
    template_name = "loan-pay.html"
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
        )

    def form_valid(self, form):
        self.debit_amount_from_bank(form.cleaned_data["principle_amount"], form.cleaned_data["date"], "Principle Loan")
        self.debit_amount_from_bank(form.cleaned_data["interest"], form.cleaned_data["date"], "Loan Interest")

        loan = LoanHistoryModel.objects.get(pk=self.kwargs['history_pk'])
        loan.amount -= form.cleaned_data["principle_amount"]
        loan.save()
        LoanHistoryModel.objects.create(
            user=self.request.user,
            bank=BankModel.objects.get(pk=self.kwargs['bank_pk']),
            date=form.cleaned_data["date"],
            from_where=form.cleaned_data["from_where"],
            amount=-form.cleaned_data["principle_amount"],
            pending_amount=loan.amount,
            is_pay=True
        )

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["entries"] = LoanHistoryModel.objects.filter(is_deleted=False, amount__lt=0)
        return context
