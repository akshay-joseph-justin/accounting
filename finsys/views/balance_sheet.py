from django.views.generic import TemplateView

from finsys import models


class BalanceSheetView(TemplateView):
    template_name = "balance_sheet.html"

    def get_context_data(self, **kwargs):
        capital = models.CapitalModel.objects.first()
        loan = models.LoanModel.objects.first()
        fixed = models.FixedAssetsModel.objects.first()
        banks = models.BankModel.objects.all()

        # Ensure objects are not None before accessing attributes
        capital_balance = capital.balance if capital else 0
        loan_balance = loan.balance if loan else 0
        fixed_assets_total = fixed.balance if fixed else 0
        bank_total = sum(bank.balance for bank in banks)

        liability_total = capital_balance + loan_balance
        assets_total = fixed_assets_total + bank_total

        return {
            "capital": capital,
            "loan": loan,
            "banks": banks,
            "fixed_asset": fixed,
            "liability_total": liability_total,
            "assets_total": assets_total,
        }
