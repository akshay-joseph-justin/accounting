from django.urls import reverse_lazy
from django.views import generic

from finsys.models import DepreciationModel, FixedAssetsHistoryModel
from finsys.forms import DepreciationForm


class AddDepreciationView(generic.CreateView):
    model = DepreciationModel
    form_class = DepreciationForm
    template_name = "add-depreciation.html"
    success_url = reverse_lazy("finsys:journal")

