from django.contrib import admin

from finsys import models


@admin.register(models.AccountModel)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'account_type', 'balance', 'is_bank', 'is_inbuilt']
    list_filter = ['code', 'name', 'account_type']
    search_fields = ['code', 'name']
    ordering = ['code', 'name', 'created_at']


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
