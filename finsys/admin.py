from django.contrib import admin

from finsys import models


@admin.register(models.AccountModel)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'account_type', 'balance', 'parent', 'is_active']
    list_filter = ['code', 'name', 'account_type', 'is_active']
    search_fields = ['code', 'name']
    ordering = ['code', 'name', 'created_at']


@admin.register(models.JournalEntryModel)
class JournalEntryAdmin(admin.ModelAdmin):
    list_display = ['reference_number', 'date', 'created_by', 'status', 'period']
    list_filter = ['date', 'created_by', 'status', 'period']
    search_fields = ['reference_number']
    ordering = ['reference_number']


@admin.register(models.JournalEntryLineModel)
class JournalEntryLineAdmin(admin.ModelAdmin):
    list_display = ['entry', 'account', 'debit_amount', 'credit_amount']
    list_filter = ['account', 'debit_amount', 'credit_amount']
    search_fields = ['account', 'debit_amount', 'credit_amount']
    ordering = ['account', 'debit_amount', 'credit_amount']


@admin.register(models.FiscalPeriodModel)
class FiscalPeriodAdmin(admin.ModelAdmin):
    list_display = ['name', 'start_date', 'end_date', 'is_closed']
    list_filter = ['start_date', 'end_date', 'is_closed']
    search_fields = ['name']


@admin.register(models.BanKModel)
class BanKAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_filter = ['name']
    search_fields = ['name']


@admin.register(models.BankTransactionModel)
class BankTransactionAdmin(admin.ModelAdmin):
    list_display = ['date', 'amount', 'bank', 'transaction_type', 'user']
    list_filter = ['date', 'bank', 'transaction_type', 'user']
    search_fields = ['date', 'bank', 'transaction_type', 'user']
    ordering = ['date', 'bank', 'transaction_type', 'user']
