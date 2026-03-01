from django.contrib import admin
from .models import EnergyListing


@admin.register(EnergyListing)
class EnergyListingAdmin(admin.ModelAdmin):
    list_display = ['title', 'producer', 'energy_type', 'quantity_kwh', 'price_per_kwh', 'status', 'created_at']
    list_filter = ['status', 'energy_type', 'created_at']
    search_fields = ['title', 'producer__username', 'location', 'description']
    readonly_fields = ['created_at']

    fieldsets = (
        ('Basic Information', {
            'fields': ('producer', 'title', 'energy_type', 'status')
        }),
        ('Quantity & Pricing', {
            'fields': ('quantity_kwh', 'price_per_kwh')
        }),
        ('Availability', {
            'fields': ('available_from', 'available_until')
        }),
        ('Location & Description', {
            'fields': ('location', 'description')
        }),
        ('Timestamps', {
            'fields': ('created_at',)
        }),
    )