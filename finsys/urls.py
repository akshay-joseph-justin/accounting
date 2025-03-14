from django.urls import path

from finsys import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),

    path("ledger/", views.AccountListView.as_view(), name="ledger"),
    path("ledger/create/", views.AccountCreateView.as_view(), name="ledger-create"),
    path("ledger/update/<int:pk>/", views.AccountUpdateView.as_view(), name="ledger-update"),
    path("ledger/delete/<int:pk>/", views.AccountDeleteView.as_view(), name="ledger-delete"),

    path("entries/create/", views.JournelEntryCreateView.as_view(), name="entries-create"),
    path("entries/update/<int:pk>/", views.JournelEntryUpdateView.as_view(), name="entries-update"),
    path("entries/delete/<int:pk>/", views.JournelEntryDeleteView.as_view(), name="entries-delete"),

    path("banks/", views.BankView.as_view(), name="wallet"),
    path("banks/<int:pk>/", views.BankDetailView.as_view(), name="bank-details"),
    path("banks/create/", views.BankCreateView.as_view(), name="bank-create"),
    path("banks/add/amount/<int:pk>/", views.BankAddAmountView.as_view(), name="bank-add-amount"),
    path("banks/edit/<int:pk>/", views.BankUpdateView.as_view(), name="bank-update"),

    path("capital/", views.CapitalView.as_view(), name="capital"),
    path("capital/amount/add/", views.CapitalCreateView.as_view(), name="capital-add-amount"),
    path("capital/edit/<int:pk>/", views.CapitalUpdateView.as_view(), name="capital-update"),
    path("capital/history/", views.CapitalHistoryView.as_view(), name="capital-history"),

    path("loan/", views.LoanView.as_view(), name="loan"),
    path("loan/amount/add/", views.LoanCreateView.as_view(), name="loan-add-amount"),
    path("loan/edit/<int:pk>/", views.LoanUpdateView.as_view(), name="loan-update"),
    path("capital/history/", views.LoanHistoryView.as_view(), name="loan-history"),

    path("withdraw/", views.WithdrawView.as_view(), name="withdraw"),
]
