from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, ListView, DetailView

from finsys.forms import LoanForm
from finsys.models import LoanModel, LoanHistoryModel


class LoanView(TemplateView):
    template_name = "loan.html"

    def get_context_data(self, **kwargs):
        loan = LoanModel.objects.all().first()
        entries = LoanHistoryModel.objects.filter(is_deleted=False)
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
        instance = LoanHistoryModel.objects.all().first()
        if instance:
            return instance.history.all()
        return LoanHistoryModel.objects.none()
