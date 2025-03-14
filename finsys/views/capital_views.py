from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, ListView

from finsys.forms.capital_forms import CapitalForm
from finsys.models import CapitalModel, CapitalHistoryModel


class CapitalView(TemplateView):
    template_name = "capital.html"

    def get_context_data(self, **kwargs):
        capital = CapitalModel.objects.all().first()
        entries = CapitalHistoryModel.objects.all()
        return {"capital": capital, 'entries': entries}


class CapitalCreateView(CreateView):
    model = CapitalHistoryModel
    form_class = CapitalForm
    template_name = "add-capital.html"
    success_url = reverse_lazy("finsys:capital")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class CapitalUpdateView(UpdateView):
    model = CapitalHistoryModel
    form_class = CapitalForm
    template_name = "add-capital.html"
    success_url = reverse_lazy("finsys:capital")


class CapitalHistoryView(ListView):
    template_name = "history.html"
    context_object_name = 'entries'
    ordering = ['-date']

    def get_queryset(self):
        instance = CapitalHistoryModel.objects.all().first()
        if instance:
            return instance.history.all()
        return CapitalHistoryModel.objects.none()
