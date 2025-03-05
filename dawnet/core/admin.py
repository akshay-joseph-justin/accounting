from django.contrib import admin

# Register your models here.
from django.contrib import admin
from . import models

admin.site.register(models.Capital)
admin.site.register(models.Liability)
admin.site.register(models.Income)

admin.site.register(models.Bank_Credit)
admin.site.register(models.Bank_Debit)

admin.site.register(models.Cash_Credit)
admin.site.register(models.Cash_Debit)

admin.site.register(models.Purchase)
admin.site.register(models.Expense)
admin.site.register(models.Asset)



