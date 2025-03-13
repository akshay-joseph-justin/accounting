from django.views import generic


class WithdrawView(generic.RedirectView):
    pattern_name = "finsys:bank-transaction-create"
