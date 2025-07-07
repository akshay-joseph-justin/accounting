from django.db.models import Sum
from django.views.generic import TemplateView

from finsys import models


class BalanceSheetView(TemplateView):
    template_name = "finsys/balance_sheet.html"

    def get_context_data(self, **kwargs):
        capital = models.CapitalModel.objects.filter(company_id=self.request.session["CURRENT_COMPANY_ID"],
                                                     year__year__exact=self.request.session["CURRENT_YEAR"]).first()
        loan = models.LoanModel.objects.filter(company_id=self.request.session["CURRENT_COMPANY_ID"],
                                               year__year__exact=self.request.session["CURRENT_YEAR"]).first()
        fixed = models.FixedAssetsModel.objects.filter(company_id=self.request.session["CURRENT_COMPANY_ID"],
                                                       year__year__exact=self.request.session["CURRENT_YEAR"]).first()
        banks = models.BankModel.objects.filter(company_id=self.request.session["CURRENT_COMPANY_ID"])

        # Ensure objects are not None before accessing attributes
        capital_balance = capital.balance if capital else 0
        loan_balance = loan.balance if loan else 0
        fixed_assets_total = \
            models.FixedAssetsHistoryModel.objects.filter(
                company_id=self.request.session["CURRENT_COMPANY_ID"],
                year__year__exact=self.request.session["CURRENT_YEAR"]).aggregate(
                total=Sum('current_balance'))['total'] or 0
        bank_total = sum(bank.balance for bank in banks)

        liability_total = capital_balance + loan_balance
        assets_total = fixed_assets_total + bank_total
        profit_loss = assets_total - liability_total
        if profit_loss > 0:
            liability_total += profit_loss
        elif profit_loss < 0:
            liability_total += profit_loss

        capital_entries = models.CapitalHistoryModel.objects.filter(
            company_id=self.request.session["CURRENT_COMPANY_ID"], is_deleted=False,
            year__year__exact=self.request.session["CURRENT_YEAR"]).values("pk",
                                                                           "from_where").annotate(
            total_amount=Sum("amount")).order_by("from_where")
        fixed_entries = models.FixedAssetsHistoryModel.objects.filter(
            company_id=self.request.session["CURRENT_COMPANY_ID"], is_deleted=False,
            year__year__exact=self.request.session["CURRENT_YEAR"]).values("pk",
                                                                           "from_where").annotate(
            total_amount=Sum("current_balance")).order_by("from_where")
        loan_entries = models.LoanHistoryModel.objects.filter(company_id=self.request.session["CURRENT_COMPANY_ID"],
                                                              is_deleted=False, amount__gt=0,
                                                              year__year__exact=self.request.session[
                                                                  "CURRENT_YEAR"]).values("pk",
                                                                                          "bank__name").annotate(
            total_amount=Sum("amount")).order_by("bank")

        return {
            "capital": capital,
            "capital_entries": capital_entries,
            "loan": loan,
            "loan_entries": loan_entries,
            "banks": banks,
            "fixed_asset": fixed,
            "fixed_entries": fixed_entries,
            "liability_total": liability_total,
            "assets_total": assets_total,
            "current_assets_total": bank_total,
            "profit_loss": profit_loss,
        }
