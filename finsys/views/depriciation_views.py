from django.urls import reverse_lazy
from django.views import generic

from finsys.models import DepreciationModel, FixedAssetsHistoryModel
from finsys.forms import DepreciationForm
from finsys.views.delete import DeleteView


class AddDepreciationView(generic.CreateView):
    model = DepreciationModel
    form_class = DepreciationForm
    template_name = "add-depreciation.html"
    success_url = reverse_lazy("finsys:journal")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

