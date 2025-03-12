from django.views.generic import DeleteView as delete_view
from .home_view import HomeView
from .account_views import (
    AccountListView,
    AccountCreateView,
    AccountUpdateView,
    AccountDeleteView
)
from .journel_enry_views import (
    JournelEntryCreateView,
    JournelEntryUpdateView,
    JournelEntryDeleteView,
)
from .wallet_views import (
    BankView,
    BankCreateView,
)
from .capital_views import (
    CapitalView,
    CapitalAddAmountView,
)
from .loan_views import (
    LoanView,
    LoanAddAmountView,
)
from .withdraw_views import WithdrawView
