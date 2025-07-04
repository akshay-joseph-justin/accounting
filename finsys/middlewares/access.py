from django.shortcuts import redirect
from django.urls import resolve, reverse_lazy

from users.models import UserCompanyModel, YearModel


class CompanyRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        resolver_match = resolve(request.path_info)
        app_name = resolver_match.app_name or resolver_match.func.__module__.split('.')[0]

        target_app = 'finsys'

        if app_name == target_app and request.user.is_authenticated:
            exempt_paths = ["finsys:company-404", "finsys:company-create"]
            if resolver_match.view_name in exempt_paths:
                return self.get_response(request)

            user_companies = UserCompanyModel.objects.filter(user=request.user)

            if not user_companies.exists():
                return redirect(reverse_lazy("finsys:company-404"))

            if not request.session.get("CURRENT_COMPANY_NAME"):
                request.session["CURRENT_COMPANY_NAME"] = user_companies.first().company.name
            if not request.session.get("CURRENT_COMPANY_ID"):
                request.session["CURRENT_COMPANY_ID"] = user_companies.first().company.id
            if not request.session.get("CURRENT_YEAR"):
                request.session["CURRENT_YEAR"] = YearModel.objects.filter(
                    company_id=request.session["CURRENT_COMPANY_ID"]).last().year
            if not request.session.get("CURRENT_YEAR_ID"):
                request.session["CURRENT_YEAR_ID"] = YearModel.objects.filter(
                    company_id=request.session["CURRENT_COMPANY_ID"]).last().id
        return self.get_response(request)
