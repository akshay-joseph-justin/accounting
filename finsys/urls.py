from django.urls import path

from finsys import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),

    path("ledger/", views.AccountListView.as_view(), name="ledger"),
    path("ledger/create/", views.AccountCreateView.as_view(), name="ledger-create"),
    path("ledger/update/<int:pk>", views.AccountUpdateView.as_view(), name="ledger-update"),
    path("ledger/delete/<int:pk>", views.AccountDeleteView.as_view(), name="ledger-delete"),

    path("entries/", views.JournelEntryListView.as_view(), name="entries-list"),
    path("entries/create/", views.JournelEntryCreateView.as_view(), name="entries-create"),
    path("entries/details/<int:pk>", views.JournelEntryListView.as_view(), name="entries-list"),
    path("entries/update/<int:pk>", views.JournelEntryUpdateView.as_view(), name="entries-update"),
    path("entries/delete/<int:pk>", views.JournelEntryDeleteView.as_view(), name="entries-delete"),

    path("wallet/", views.WalletView.as_view(), name="wallet"),
]
