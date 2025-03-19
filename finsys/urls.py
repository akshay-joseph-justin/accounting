from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from finsys import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),

    path("login/", LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),

    path("ledger/", views.AccountListView.as_view(), name="ledger"),
    path("ledger/create/", views.AccountCreateView.as_view(), name="ledger-create"),
    path("ledger/update/<int:pk>/", views.AccountUpdateView.as_view(), name="ledger-update"),
    path("ledger/delete/<int:pk>/", views.AccountDeleteView.as_view(), name="ledger-delete"),
    path("ledger/<int:pk>/", views.AccountDetailView.as_view(), name="ledger-details"),

    path("entries/create/<int:pk>/", views.AccountHistoryCreateView.as_view(), name="entries-create"),
    path("entries/update/<int:pk>/", views.AccountHistoryUpdateView.as_view(), name="entries-update"),
    path("entries/history/<int:pk>/", views.AccountHistoryView.as_view(), name="entries-history"),

    path("banks/", views.BankView.as_view(), name="wallet"),
    path("banks/<int:pk>/", views.BankDetailView.as_view(), name="bank-details"),
    path("banks/create/", views.BankCreateView.as_view(), name="bank-create"),
    path("banks/add/amount/<int:pk>/", views.BankAddAmountView.as_view(), name="bank-add-amount"),
    path("banks/edit/<int:pk>/", views.BankUpdateView.as_view(), name="bank-update"),

    path("banks/transfer/", views.BankTransferListView.as_view(), name="bank-transfer"),
    path("banks/transfer/create/", views.BankTransferView.as_view(), name="bank-transfer-create"),

    path("capital/", views.CapitalView.as_view(), name="capital"),
    path("capital/<int:pk>/", views.CapitalDetailView.as_view(), name="capital-details"),
    path("capital/amount/add/", views.CapitalCreateView.as_view(), name="capital-add-amount"),
    path("capital/edit/<int:pk>/", views.CapitalUpdateView.as_view(), name="capital-update"),
    path("capital/history/", views.CapitalHistoryView.as_view(), name="capital-history"),

    path("loan/", views.LoanView.as_view(), name="loan"),
    path("loan/<int:pk>/", views.LoanDetailView.as_view(), name="loan-details"),
    path("loan/amount/add/", views.LoanCreateView.as_view(), name="loan-add-amount"),
    path("loan/edit/<int:pk>/", views.LoanUpdateView.as_view(), name="loan-update"),
    path("loan/history/", views.LoanHistoryView.as_view(), name="loan-history"),
    path("loan/pay/<int:pk>", views.LoanPayView.as_view(), name="loan-pay"),

    path("fixed-assets/", views.FixedAssetsView.as_view(), name="fixed-assets"),
    path("fixed-assets/<int:pk>/", views.FixedAssetsDetailView.as_view(), name="fixed-assets-details"),
    path("fixed-assets/create/", views.FixedAssetsCreateView.as_view(), name="fixed-assets-create"),
    path("fixed-assets/update/<int:pk>/", views.FixedAssetsUpdateView.as_view(), name="fixed-assets-update"),
    path("fixed-assets/update/depreciation/<int:pk>/", views.FixedAssetsDepreciationUpdateView.as_view(), name="fixed-assets-depreciation"),
    path("fixed-assets/history/<int:pk>/", views.FixedAssetsHistoryView.as_view(), name="fixed-assets-history"),

    path("balance-sheet/", views.BalanceSheetView.as_view(), name="balance-sheet"),

]
