from django.contrib import admin
from .models import Plan, Subscription

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'id', 'price', 'duration_days', 'created_at','updated_at']
    list_filter = ['duration_days', 'created_at']
    search_fields = ['name']
    ordering = ['price']

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'id',  'plan', 'status', 'start_date', 'end_date', 'created_at', 'updated_at']
    list_filter = ['status', 'created_at', 'plan']
    search_fields = ['user__username', 'user__email', 'plan__name']
    raw_id_fields = ['user', 'plan']
    readonly_fields = ['created_at', 'updated_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'plan')
