from django.urls import path

from . import views

urlpatterns = [
    path("404/", views.CompanyNotFound.as_view(), name="company-404"),
    path("create/", views.CompanyCreateView.as_view(), name="company-create"),
    path("switch/", views.SwitchCompanyView.as_view(), name="company-switch"),
    path("detail/<name>/", views.CompanyDetailView.as_view(), name="company-detail"),
    path("update/<pk>/", views.CompanyUpdateView.as_view(), name="company-update"),
    path("delete/<pk>/", views.CompanyDeleteView.as_view(), name="company-delete"),
    path("member/add/<pk>/", views.MemberCreateView.as_view(), name="company-member-add"),
    path("member/role/change/<pk>/", views.MemberRoleChangeView.as_view(), name="company-role-change"),
    path("member/remove/<pk>/", views.MemberRoleChangeView.as_view(), name="company-member-remove"),


    path("switch/year/", views.YearSwitchView.as_view(), name="company-year-switch"),
]