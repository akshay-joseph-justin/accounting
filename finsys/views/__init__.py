from .account_views import (
    AccountListView,
    AccountCreateView,
    AccountUpdateView,
    AccountDeleteView,
    AccountDetailView,

    AccountHistoryView,
    AccountHistoryCreateView,
    AccountHistoryUpdateView,
    AccountHistoryDeleteView,
)
from .capital_views import (
    CapitalView,
    CapitalDetailView,
    CapitalCreateView,
    CapitalUpdateView,
    CapitalHistoryView,
    CapitalDeleteView,
)
from .home_view import HomeView
from .loan_views import (
    LoanView,
    LoanDetailView,
    LoanCreateView,
    LoanUpdateView,
    LoanHistoryView,
    LoanPayView,
    LoanDeleteView
)
from .bank_views import (
    BankView,
    BankCreateView,
    BankDetailView,
    BankUpdateView,
    BankDeleteView,

    BankAddAmountView,
    BankTransactionDeleteView,

    BankTransferView,
    BankTransferListView,
    BankTransferDeleteView,

)
from .fixed_assets_views import (
    FixedAssetsView,
    FixedAssetsDetailView,
    FixedAssetsCreateView,
    FixedAssetsUpdateView,
    FixedAssetsDeleteView,
    FixedAssetsHistoryView,
)
from .balance_sheet import BalanceSheetView
from .trial_balance_views import TrialBalanceView, ProfitLossApi
from .reciept_payment_views import ReceiptView, PaymentView
from .journal_views import (
    JournalListView,
    JournalCreateView,
    JournalUpdateView,
    JournalDeleteView,
)
from .depriciation_views import AddDepreciationView
