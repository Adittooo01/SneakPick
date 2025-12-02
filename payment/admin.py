from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """Admin interface for the Payment model."""
    
    list_display = (
        'id',
        'user',
        'order',
        'amount',
        'method',
        'status',
        'payment_date',
        'transaction_id',
    )
    
    list_filter = ('status', 'method', 'payment_date')
    search_fields = ('user__username', 'order__id', 'transaction_id')
