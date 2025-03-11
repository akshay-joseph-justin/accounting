from django.db.models import Sum
from django.views.generic import TemplateView

from finsys.models import BanKModel, BankTransactionModel


class CapitalView(TemplateView):
    template_name = "capital.html"

    def get_context_data(self, **kwargs):
        total_capital = BanKModel.objects.all().aggregate(total_capital=Sum('capital'))['total_capital']
        banks = BanKModel.objects.all()
        return {"banks": banks, "total_capital": total_capital}
