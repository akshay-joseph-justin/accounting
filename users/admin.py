from django.contrib import admin

from . import models

admin.site.register(models.User)
admin.site.register(models.OTPModel)
admin.site.register(models.TokenModel)

@admin.register(models.CompanyModel)
class CompanyModelAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(models.UserCompanyModel)
class UserCompanyModelAdmin(admin.ModelAdmin):
    list_display = ["user", "company"]

