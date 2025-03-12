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

    path("wallet/", views.BankView.as_view(), name="wallet"),
    path("wallet/create/bank/", views.BankCreateView.as_view(), name="bank-create"),

    path("capital/", views.CapitalView.as_view(), name="capital"),
    path("capital/amount/add/", views.CapitalAddAmountView.as_view(), name="capital-add-amount"),

    path("loan/", views.LoanView.as_view(), name="loan"),
    path("loan/amount/add/", views.LoanAddAmountView.as_view(), name="loan-add-amount"),

    path("withdraw/", views.WithdrawView.as_view(), name="withdraw"),
]
