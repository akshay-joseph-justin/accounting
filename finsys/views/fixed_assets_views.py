from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, ListView

from finsys.forms import FixedAssetsCreateForm, FixedAssetsUpdateForm
from finsys.models import FixedAssetsModel, FixedAssetsHistoryModel


class FixedAssetsView(TemplateView):
    template_name = "fixed-assets.html"

    def get_context_data(self, **kwargs):
        fixed_asset = FixedAssetsModel.objects.all().first()
        entries = FixedAssetsHistoryModel.objects.filter(is_deleted=False)
        return {"fixed_asset": fixed_asset, 'entries': entries}


class FixedAssetsCreateView(CreateView):
    model = FixedAssetsHistoryModel
    form_class = FixedAssetsCreateForm
    template_name = "add-capital.html"
    success_url = reverse_lazy("finsys:fixed-assets")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class FixedAssetsUpdateView(UpdateView):
    model = FixedAssetsHistoryModel
    form_class = FixedAssetsUpdateForm
    template_name = "add-capital.html"
    success_url = reverse_lazy("finsys:fixed-assets")


class FixedAssetsHistoryView(ListView):
    template_name = "fixed-asset-history.html"
    context_object_name = 'entries'
    ordering = ['-date']

    def get_queryset(self):
        instance = FixedAssetsHistoryModel.objects.filter(pk=self.kwargs['pk']).first()
        if instance:
            return instance.history.all()
        return FixedAssetsHistoryModel.objects.none()
