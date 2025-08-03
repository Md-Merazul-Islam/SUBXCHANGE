from django.contrib import admin
from .models import ExchangeRateLog

@admin.register(ExchangeRateLog)
class ExchangeRateLogAdmin(admin.ModelAdmin):
    list_display = ['base_currency', 'target_currency', 'rate', 'fetched_at']
    list_filter = ['base_currency', 'target_currency', 'fetched_at']
    search_fields = ['base_currency', 'target_currency']
    readonly_fields = ['fetched_at']
    ordering = ['-fetched_at']