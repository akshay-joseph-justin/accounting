from django.db.models import Sum
from django.views.generic import TemplateView

from finsys.models import BanKModel


class LoanView(TemplateView):
    template_name = "loan.html"

    def get_context_data(self, **kwargs):
        total_loan = BanKModel.objects.all().aggregate(total_loan=Sum('loan'))['total_loan']
        banks = BanKModel.objects.all()
        return {"banks": banks, "total_loan": total_loan}
