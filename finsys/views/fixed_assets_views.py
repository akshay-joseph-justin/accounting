from django.db.models import Sum
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, ListView, DetailView

from finsys.forms import FixedAssetsCreateForm, FixedAssetsUpdateForm
from finsys.models import FixedAssetsModel, FixedAssetsHistoryModel, BankTransactionModel
from finsys.views.delete import DeleteView


class FixedAssetsView(TemplateView):
    template_name = "finsys/fixed-assets.html"

    def get_context_data(self, **kwargs):
        fixed_asset = FixedAssetsModel.objects.filter(company_id=self.request.session["CURRENT_COMPANY_ID"],
                                                      year_id=self.request.session["CURRENT_YEAR_ID"]).first()
        entries = FixedAssetsHistoryModel.objects.filter(is_deleted=False,
                                                         company=self.request.session["CURRENT_COMPANY_ID"],
                                                         year_id=self.request.session["CURRENT_YEAR_ID"]).annotate(
            total=Sum('current_balance'))
        return {"fixed_asset": fixed_asset, 'entries': entries}


class FixedAssetsDetailView(DetailView):
    template_name = "finsys/capital-details.html"
    context_object_name = "ledger"

    def get_queryset(self):
        return FixedAssetsHistoryModel.objects.filter(is_deleted=False, year_id=self.request.session["CURRENT_YEAR_ID"],
                                                      company_id=self.request.session["CURRENT_COMPANY_ID"])


class FixedAssetsCreateView(CreateView):
    model = FixedAssetsHistoryModel
    form_class = FixedAssetsCreateForm
    template_name = "finsys/add-fixed.html"
    success_url = reverse_lazy("finsys:fixed-assets")

    def get_initial(self):
        return {"company": self.request.session["CURRENT_COMPANY_ID"]}

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.company_id = self.request.session["CURRENT_COMPANY_ID"]
        form.instance.year_id = self.request.session["CURRENT_YEAR_ID"]
        return super().form_valid(form)


class FixedAssetsUpdateView(UpdateView):
    model = FixedAssetsHistoryModel
    form_class = FixedAssetsUpdateForm
    template_name = "finsys/add-fixed.html"
    success_url = reverse_lazy("finsys:fixed-assets")


class FixedAssetsDeleteView(DeleteView):
    model = FixedAssetsHistoryModel
    success_url = reverse_lazy("finsys:fixed-assets")

    def get(self, request, *args, **kwargs):
        asset = FixedAssetsModel.objects.filter(year_id=self.request.session["CURRENT_YEAR_ID"],
                                                company_id=self.request.session["CURRENT_COMPANY_ID"]).first()
        entry = FixedAssetsHistoryModel.objects.filter(pk=kwargs['pk']).first()
        asset.balance -= entry.amount
        asset.save()
        BankTransactionModel.objects.filter(foreign_id=entry.id, head__iexact="Fixed Asset").update(is_deleted=True)

        return super().get(request, *args, **kwargs)


class FixedAssetsHistoryView(ListView):
    template_name = "finsys/fixed-asset-history.html"
    context_object_name = 'entries'
    ordering = ['-date']

    def get_queryset(self):
        instance = FixedAssetsHistoryModel.objects.filter(pk=self.kwargs['pk'],
                                                          company=self.request.session["CURRENT_COMPANY_ID"],
                                                          year_id=self.request.session["CURRENT_YEAR_ID"]).first()
        if instance:
            return instance.history.all()
        return FixedAssetsHistoryModel.objects.none()
