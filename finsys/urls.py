from django.urls import path

from finsys import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),

    path("accounts/", views.AccountListView.as_view(), name="account-list"),
    path("accounts/create/", views.AccountCreateView.as_view(), name="account-create"),
    path("accounts/update/<int:pk>", views.AccountUpdateView.as_view(), name="account-update"),
    path("accounts/delete/<int:pk>", views.AccountDeleteView.as_view(), name="account-delete"),

    path("entries/", views.JournelEntryListView.as_view(), name="entries-list"),
    path("entries/create/", views.JournelEntryCreateView.as_view(), name="entries-create"),
    path("entries/details/<int:pk>", views.JournelEntryListView.as_view(), name="entries-list"),
    path("entries/update/<int:pk>", views.JournelEntryUpdateView.as_view(), name="entries-update"),
    path("entries/delete/<int:pk>", views.JournelEntryDeleteView.as_view(), name="entries-delete"),
]
