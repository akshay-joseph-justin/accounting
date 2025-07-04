from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, ListView, DetailView

from finsys.forms.capital_forms import CapitalForm
from finsys.models import CapitalModel, CapitalHistoryModel, BankTransactionModel
from finsys.views.delete import DeleteView


class CapitalView(TemplateView):
    template_name = "finsys/capital.html"

    def get_context_data(self, **kwargs):
        capital = CapitalModel.objects.filter(company_id=self.request.session["CURRENT_COMPANY_ID"],
                                              year_id=self.request.session["CURRENT_YEAR_ID"]).first()
        entries = CapitalHistoryModel.objects.filter(is_deleted=False,
                                                     company_id=self.request.session["CURRENT_COMPANY_ID"],
                                                     year_id=self.request.session["CURRENT_YEAR_ID"])
        return {"capital": capital, 'entries': entries}


class CapitalDetailView(DetailView):
    template_name = "finsys/capital-details.html"
    context_object_name = "ledger"

    def get_queryset(self):
        return CapitalHistoryModel.objects.filter(is_deleted=False,
                                                  company_id=self.request.session["CURRENT_COMPANY_ID"],
                                                  year_id=self.request.session["CURRENT_YEAR_ID"])


class CapitalCreateView(CreateView):
    model = CapitalHistoryModel
    form_class = CapitalForm
    template_name = "finsys/add-capital.html"
    success_url = reverse_lazy("finsys:capital")

    def get_initial(self):
        return {
            "company_id": self.request.session["CURRENT_COMPANY_ID"]
        }

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.company_id = self.request.session["CURRENT_COMPANY_ID"]
        form.instance.year_id = self.request.session["CURRENT_YEAR_ID"]
        return super().form_valid(form)


class CapitalUpdateView(UpdateView):
    model = CapitalHistoryModel
    form_class = CapitalForm
    template_name = "finsys/add-capital.html"
    success_url = reverse_lazy("finsys:capital")


class CapitalDeleteView(DeleteView):
    model = CapitalHistoryModel
    success_url = reverse_lazy("finsys:capital")

    def get(self, request, *args, **kwargs):
        capital = CapitalModel.objects.filter(company_id=request.session["CURRENT_COMPANY_ID"],
                                              year_id=self.request.session["CURRENT_YEAR_ID"]).first()
        entry = CapitalHistoryModel.objects.filter(pk=kwargs['pk']).first()
        capital.balance -= entry.amount
        capital.save()
        BankTransactionModel.objects.filter(foreign_id=entry.id, head__iexact="Capital").update(is_deleted=True)

        return super().get(request, *args, **kwargs)


class CapitalHistoryView(ListView):
    template_name = "finsys/history.html"
    context_object_name = 'entries'
    ordering = ['-date']

    def get_queryset(self):
        instance = CapitalHistoryModel.objects.get(pk=self.kwargs['pk'])
        if instance:
            return instance.history.all()
        return CapitalHistoryModel.objects.none()
