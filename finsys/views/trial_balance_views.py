from datetime import datetime, timedelta
from itertools import chain

from django.db.models import Sum
from django.http import JsonResponse
from django.views import View
from django.views.generic import ListView

from finsys.models import BankTransactionModel, BankModel, DepreciationModel


class TrialBalanceView(ListView):
    context_object_name = 'transactions'
    template_name = 'finsys/trial-balance.html'

    def profit_loss(self):
        total_debit = \
            BankTransactionModel.objects.filter(transaction_type=BankTransactionModel.DEBIT,
                                                is_deleted=False,
                                                bank__company_id=self.request.session["CURRENT_COMPANY_ID"],
                                                year_id=self.request.session["CURRENT_YEAR_ID"]).aggregate(
                total=Sum('amount'))[
                "total"] or 0
        total_credit = \
            BankTransactionModel.objects.filter(transaction_type=BankTransactionModel.CREDIT, is_deleted=False,
                                                bank__company_id=self.request.session["CURRENT_COMPANY_ID"],
                                                year_id=self.request.session["CURRENT_YEAR_ID"]).aggregate(
                total=Sum('amount'))["total"] or 0
        amount = total_credit - total_debit
        if amount < 0:
            return amount, "Loss"
        elif amount > 0:
            return amount, "Profit"
        return amount, "Balanced"

    def get_queryset(self):
        bank = BankTransactionModel.objects.filter(is_deleted=False,
                                                   bank__company_id=self.request.session["CURRENT_COMPANY_ID"],
                                                   year_id=self.request.session["CURRENT_YEAR_ID"]).order_by("date")
        depreciation = DepreciationModel.objects.filter(
            asset__bank__company_id=self.request.session["CURRENT_COMPANY_ID"],
            asset__year_id=self.request.session["CURRENT_YEAR_ID"]).order_by("date")
        combined_queryset = chain(bank, depreciation)
        return sorted(combined_queryset, key=lambda x: x.date)

    def get_context_data(self, **kwargs):
        context = super(TrialBalanceView, self).get_context_data(**kwargs)
        context["total"] = \
        BankModel.objects.filter(company_id=self.request.session["CURRENT_COMPANY_ID"]).aggregate(total=Sum("balance"))[
            "total"]
        context["banks"] = BankModel.objects.filter(company_id=self.request.session["CURRENT_COMPANY_ID"])
        amount, status = self.profit_loss()
        context["amount"] = abs(amount)
        context["status"] = status
        return context


class ProfitLossApi(View):

    def get(self, request):
        # Get the date parameters from the GET request
        single_date = request.GET.get('date', None)
        start_date = request.GET.get('start', None)
        end_date = request.GET.get('end', None)

        # Prepare the query filter
        filters = {}

        # Apply single date filter (ignoring day, only filtering by month and year)
        if single_date:
            try:
                # Parse the provided single_date to datetime
                single_date = datetime.strptime(single_date, '%Y-%m-%d')

                # Get the first and last day of the given month
                start_of_month = single_date.replace(day=1)
                end_of_month = single_date.replace(day=1).replace(month=single_date.month % 12 + 1) - timedelta(days=1)

                # Apply the month range filter
                filters['date__range'] = [start_of_month, end_of_month]

            except ValueError:
                return JsonResponse({'error': 'Invalid date format for singleDate'}, status=400)

        # Apply date range filter if `start_date` and `end_date` are provided
        if start_date and end_date:
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d')
                end_date = datetime.strptime(end_date, '%Y-%m-%d')
                filters['date__range'] = [start_date, end_date]
            except ValueError:
                return JsonResponse({'error': 'Invalid date format for start or end date'}, status=400)

        # Query to calculate the total debit amount (filtered by dates if provided)
        total_debit = \
            BankTransactionModel.objects.filter(transaction_type=BankTransactionModel.DEBIT, **filters).aggregate(
                total=Sum('amount'))["total"] or 0

        # Query to calculate the total credit amount (filtered by dates if provided)
        total_credit = \
            BankTransactionModel.objects.filter(transaction_type=BankTransactionModel.CREDIT, **filters).aggregate(
                total=Sum('amount'))["total"] or 0

        # Calculate profit or loss
        amount = total_credit - total_debit

        if amount < 0:
            return JsonResponse({"status": f"Loss - {amount}"}, status=200)
        elif amount > 0:
            return JsonResponse({"status": f"Profit - {amount}"}, status=200)
        return JsonResponse({"status": "Balanced"}, status=200)
