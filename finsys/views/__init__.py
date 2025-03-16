from .account_views import (
    AccountListView,
    AccountCreateView,
    AccountUpdateView,
    AccountDeleteView,
    AccountDetailView,

    AccountHistoryView,
    AccountHistoryCreateView,
    AccountHistoryUpdateView
)
from .capital_views import (
    CapitalView,
    CapitalCreateView,
    CapitalUpdateView,
    CapitalHistoryView,
)
from .home_view import HomeView
from .loan_views import (
    LoanView,
    LoanCreateView,
    LoanUpdateView,
    LoanHistoryView,
)
from .bank_views import (
    BankView,
    BankCreateView,
    BankDetailView,
    BankUpdateView,
    BankAddAmountView,

    BankTransferView,
    BankTransferListView,

)
from .fixed_assets_views import (
    FixedAssetsView,
    FixedAssetsCreateView,
    FixedAssetsUpdateView,
    FixedAssetsHistoryView
)
from .balance_sheet import BalanceSheetView
