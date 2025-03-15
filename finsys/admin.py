from django.contrib import admin

from finsys import models


@admin.register(models.AccountModel)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['name', 'account_type', 'balance']
    list_filter = ['name', 'account_type']
    search_fields = ['name']
    ordering = ['name', 'created_at']


class JournalEntryLineInline(admin.TabularInline):
    model = models.JournalEntryLineModel
    extra = 1


@admin.register(models.JournalEntryModel)
class JournalEntryAdmin(admin.ModelAdmin):
    list_display = ['reference_number', 'date', 'created_by']
    list_filter = ['date', 'created_by']
    search_fields = ['reference_number']
    ordering = ['reference_number']
    inlines = [JournalEntryLineInline]


@admin.register(models.BankModel)
class BankModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'account_number', 'branch', 'balance']
    list_filter = ['account_number', 'branch']
    search_fields = ['name']
    ordering = ['account_number', 'branch']


@admin.register(models.BankTransactionModel)
class BankTransactionModelAdmin(admin.ModelAdmin):
    list_display = ['bank', 'date', 'head', 'from_where', 'transaction_type', 'amount']
    list_filter = ['bank', 'date', 'from_where', 'transaction_type', 'amount']
    search_fields = ['bank', 'head', 'from_where']


@admin.register(models.CapitalHistoryModel)
class CapitalModelAdmin(admin.ModelAdmin):
    list_display = ['date', 'from_where', 'bank', 'amount']
    list_filter = ['date', 'from_where', 'bank', 'amount']
    search_fields = ['date', 'from_where', 'bank', 'amount']
    ordering = ['date', 'from_where', 'bank', 'amount']


@admin.register(models.CapitalModel)
class CapitalModelAdmin(admin.ModelAdmin):
    list_display = ["balance"]


@admin.register(models.LoanModel)
class LoanModelAdmin(admin.ModelAdmin):
    list_display = ['balance']


@admin.register(models.LoanHistoryModel)
class LoanHistoryModelAdmin(admin.ModelAdmin):
    list_display = ['date', 'from_where', 'bank', 'amount']
    list_filter = ['date', 'from_where', 'bank', 'amount']
    search_fields = ['date', 'from_where', 'bank', 'amount']
    ordering = ['date', 'from_where', 'bank', 'amount']





