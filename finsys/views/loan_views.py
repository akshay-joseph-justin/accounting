from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, ListView

from finsys import generate_random_number
from finsys.forms import LoanForm
from finsys.models import LoanModel, LoanHistoryModel


class LoanView(TemplateView):
    template_name = "loan.html"

    def get_context_data(self, **kwargs):
        loan = LoanModel.objects.all().first()
        entries = LoanHistoryModel.objects.all()
        return {"loan": loan, "entries": entries}

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


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
    model = LoanHistoryModel
    template_name = "history.html"
    context_object_name = 'entries'
    ordering = ['-date']
