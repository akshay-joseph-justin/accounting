from django.db.models import Sum
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, ListView, DetailView

from finsys.forms import FixedAssetsCreateForm, FixedAssetsUpdateForm, DepreciationForm
from finsys.models import FixedAssetsModel, FixedAssetsHistoryModel, BankTransactionModel
from finsys.views.delete import DeleteView


class FixedAssetsView(TemplateView):
    template_name = "fixed-assets.html"

    def get_context_data(self, **kwargs):
        fixed_asset = FixedAssetsModel.objects.all().first()
        entries = FixedAssetsHistoryModel.objects.filter(is_deleted=False).annotate(total=Sum('current_balance'))
        return {"fixed_asset": fixed_asset, 'entries': entries}


class FixedAssetsDetailView(DetailView):
    template_name = "capital-details.html"
    context_object_name = "ledger"

    def get_queryset(self):
        return FixedAssetsHistoryModel.objects.filter(is_deleted=False)


class FixedAssetsCreateView(CreateView):
    model = FixedAssetsHistoryModel
    form_class = FixedAssetsCreateForm
    template_name = "add-fixed.html"
    success_url = reverse_lazy("finsys:fixed-assets")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class FixedAssetsUpdateView(UpdateView):
    model = FixedAssetsHistoryModel
    form_class = FixedAssetsUpdateForm
    template_name = "add-fixed.html"
    success_url = reverse_lazy("finsys:fixed-assets")


class FixedAssetsDeleteView(DeleteView):
    model = FixedAssetsHistoryModel
    success_url = reverse_lazy("finsys:fixed-assets")

    def get(self, request, *args, **kwargs):
        asset = FixedAssetsModel.objects.all().first()
        entry = FixedAssetsHistoryModel.objects.filter(pk=kwargs['pk']).first()
        asset.balance -= entry.amount
        asset.save()
        BankTransactionModel.objects.filter(foreign_id=entry.id, head__iexact="Fixed Asset").update(is_deleted=True)

        return super().get(request, *args, **kwargs)


class FixedAssetsHistoryView(ListView):
    template_name = "fixed-asset-history.html"
    context_object_name = 'entries'
    ordering = ['-date']

    def get_queryset(self):
        instance = FixedAssetsHistoryModel.objects.filter(pk=self.kwargs['pk']).first()
        if instance:
            return instance.history.all()
        return FixedAssetsHistoryModel.objects.none()
