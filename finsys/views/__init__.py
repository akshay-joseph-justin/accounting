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
from .journel_enry_views import (
    JournelEntryCreateView,
    JournalEntryUpdateView,
    JournalEntryHistoryView,
)
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
from .withdraw_views import WithdrawView
