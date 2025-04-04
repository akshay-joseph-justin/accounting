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
    CapitalDetailView,
    CapitalCreateView,
    CapitalUpdateView,
    CapitalHistoryView,
)
from .home_view import HomeView
from .loan_views import (
    LoanView,
    LoanDetailView,
    LoanCreateView,
    LoanUpdateView,
    LoanHistoryView,
    LoanPayView,
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
    FixedAssetsDetailView,
    FixedAssetsCreateView,
    FixedAssetsUpdateView,
    FixedAssetsHistoryView,
)
from .balance_sheet import BalanceSheetView
from .trial_balance_views import TrialBalanceView, ProfitLossApi
from .reciept_payment_views import ReceiptView, PaymentView
from .journal_views import (
    JournalListView,
    JournalCreateView,
    JournalUpdateView,
)
from .depriciation_views import AddDepreciationView
