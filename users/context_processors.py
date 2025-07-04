from datetime import datetime

from django.conf import settings

from users.models import UserCompanyModel, YearModel


def get_user_companies(request):
    if not request.user.is_authenticated:
        return []

    current_company = request.session.get("CURRENT_COMPANY_NAME")

    return UserCompanyModel.objects.filter(
        user=request.user
    ).exclude(
        company__name=current_company
    ).values_list('company__name', flat=True)


def is_viewer(request):
    if not request.user.is_authenticated:
        return False

    user = UserCompanyModel.objects.filter(company__name=request.session.get("CURRENT_COMPANY_NAME"),
                                                     user=request.user).first()
    if user:
        if user.role == UserCompanyModel.VIEWER:
            return False
    return True


def global_settings(request):
    return {
        'SITE_NAME': getattr(settings, 'SITE_NAME', None),
        'YEAR': datetime.now().year,
        'COMPANIES': get_user_companies(request),
        'NOT_VIEWER': is_viewer(request),
        'COMPANY_YEARS': YearModel.objects.filter(company_id=request.session.get("CURRENT_COMPANY_ID")),
    }
