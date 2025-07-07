import datetime

from django.contrib.auth import get_user_model
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views import generic

from finsys.company import forms
from finsys.models import CapitalModel, LoanModel, FixedAssetsModel
from users import models
from users.models import YearModel


class CompanyNotFound(generic.TemplateView):
    template_name = "finsys/company/company_404.html"


class CompanyCreateView(SuccessMessageMixin, generic.CreateView):
    model = models.CompanyModel
    form_class = forms.CompanyCreateForm
    template_name = "finsys/company/create.html"
    success_message = "Company created successfully"
    success_url = reverse_lazy("finsys:home")

    def form_valid(self, form):
        self.object = form.save()
        models.UserCompanyModel.objects.create(
            user=get_user_model().objects.get(pk=self.request.user.pk),
            company=self.object,
            role=models.UserCompanyModel.ADMIN
        )

        year_object, _ = models.YearModel.objects.get_or_create(company_id=self.object.pk, year=datetime.date.today().year)

        CapitalModel.objects.create(company=self.object, year_id=year_object.pk)
        LoanModel.objects.create(company=self.object, year_id=year_object.pk)
        FixedAssetsModel.objects.create(company=self.object, year_id=year_object.pk)
        return super(CompanyCreateView, self).form_valid(form)


class SwitchCompanyView(generic.RedirectView):
    pattern_name = "finsys:home"

    def get(self, request, *args, **kwargs):
        company = models.CompanyModel.objects.get(name=self.request.GET.get("c_name"))
        self.request.session["CURRENT_COMPANY_ID"] = company.id
        self.request.session["CURRENT_COMPANY_NAME"] = company.name
        return super(SwitchCompanyView, self).get(request, *args, **kwargs)


class CompanyDetailView(generic.DetailView):
    model = models.CompanyModel
    context_object_name = "company"
    template_name = "finsys/company/details.html"
    slug_field = "name"
    slug_url_kwarg = "name"

    def get_context_data(self, **kwargs):
        context = super(CompanyDetailView, self).get_context_data(**kwargs)
        context["members"] = models.UserCompanyModel.objects.filter(
            company_id=self.request.session["CURRENT_COMPANY_ID"])
        return context


class CompanyUpdateView(SuccessMessageMixin, generic.UpdateView):
    model = models.CompanyModel
    form_class = forms.CompanyCreateForm
    template_name = "finsys/company/update.html"
    success_message = "Company updated successfully"

    def get_success_url(self):
        return reverse_lazy("finsys:company-detail", kwargs={"pk": self.object.company.id})


class CompanyDeleteView(generic.DeleteView):
    model = models.CompanyModel
    success_url = reverse_lazy("finsys:home")

    def get(self, request, *args, **kwargs):
        return super(CompanyDeleteView, self).delete(request, *args, **kwargs)


class MemberCreateView(generic.CreateView):
    model = models.UserCompanyModel
    form_class = forms.MemberCreateForm
    template_name = "finsys/company/member-add.html"

    def get_success_url(self):
        return reverse_lazy("finsys:company-detail", kwargs={"name": self.object.company.name})

    def form_valid(self, form):
        form.instance.company = models.CompanyModel.objects.get(pk=self.kwargs["pk"])
        return super(MemberCreateView, self).form_valid(form)


class MemberRoleChangeView(SuccessMessageMixin, generic.UpdateView):
    model = models.UserCompanyModel
    form_class = forms.MemberRoleChangeForm
    template_name = "finsys/company/change-role.html"
    success_message = "Member role changed successfully"

    def get_success_url(self):
        return reverse_lazy("finsys:company-detail", kwargs={"name": self.object.company.name})


class MemberRemoveView(SuccessMessageMixin, generic.DeleteView):
    model = models.UserCompanyModel
    success_message = "Member role removed successfully"

    def get_success_url(self):
        return reverse_lazy("finsys:company-detail", kwargs={"name": self.object.company.name})

    def get(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class YearSwitchView(generic.RedirectView):
    pattern_name = "finsys:home"

    def get(self, request, *args, **kwargs):
        year_object = YearModel.objects.get(year=self.request.GET.get("year"))
        self.request.session["CURRENT_YEAR_ID"] = year_object.id
        return super(YearSwitchView, self).get(request, *args, **kwargs)
