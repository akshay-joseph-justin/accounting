from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from users.second_factor_auth.mixins import MultiFactorVerificationRequiredMixin

class HomeView(LoginRequiredMixin, MultiFactorVerificationRequiredMixin, TemplateView):
    template_name = "finsys/index.html"
