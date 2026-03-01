from django.contrib import admin
from .models import InvestmentProject, Investment


@admin.register(InvestmentProject)
class InvestmentProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'energy_type', 'total_funding_required', 'funding_raised', 'status', 'created_at']
    list_filter = ['status', 'energy_type', 'created_at']
    search_fields = ['title', 'description', 'location']
    readonly_fields = ['funding_raised', 'created_at']

    fieldsets = (
        ('Project Information', {
            'fields': ('title', 'description', 'energy_type', 'location', 'capacity_kw')
        }),
        ('Funding Details', {
            'fields': ('total_funding_required', 'funding_raised', 'expected_roi_percent')
        }),
        ('Timeline', {
            'fields': ('project_duration_months', 'start_date', 'expected_completion')
        }),
        ('Additional', {
            'fields': ('status', 'project_document', 'created_by', 'created_at')
        }),
    )


@admin.register(Investment)
class InvestmentAdmin(admin.ModelAdmin):
    list_display = ['investor', 'project', 'amount', 'expected_return', 'actual_return', 'status', 'investment_date']
    list_filter = ['status', 'investment_date']
    search_fields = ['investor__username', 'project__title']
    readonly_fields = ['investment_date', 'created_at']