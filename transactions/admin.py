from django.contrib import admin
from .models import Order, Transaction


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'consumer', 'listing', 'quantity_kwh', 'total_amount', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['consumer__username', 'transaction_id']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Order Information', {
            'fields': ('consumer', 'listing', 'quantity_kwh', 'total_amount', 'status')
        }),
        ('Payment Details', {
            'fields': ('payment_method', 'transaction_id')
        }),
        ('Additional Info', {
            'fields': ('notes', 'created_at', 'updated_at')
        }),
    )


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'transaction_type', 'amount', 'from_user', 'to_user', 'is_successful', 'created_at']
    list_filter = ['transaction_type', 'is_successful', 'created_at']
    search_fields = ['gateway_transaction_id', 'from_user__username', 'to_user__username']
    readonly_fields = ['created_at']