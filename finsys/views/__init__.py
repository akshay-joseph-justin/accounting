from django.views.generic import DeleteView as delete_view
from .home_view import HomeView
from .account_views import (
    AccountListView,
    AccountCreateView,
    AccountUpdateView,
    AccountDeleteView
)
from .journel_enry_views import (
    JournelEntryListView,
    JournelEntryDetailView,
    JournelEntryCreateView,
    JournelEntryUpdateView,
    JournelEntryDeleteView,
)
from .wallet_views import (
    WalletView,
)
