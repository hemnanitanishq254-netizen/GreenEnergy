from django.db import models
from django.core.validators import MinValueValidator
from accounts.models import User
from marketplace.models import EnergyListing


class Order(models.Model):
    """Energy purchase order"""
    STATUS_CHOICES = (
        ('pending', '⏳ Pending'),
        ('confirmed', '✅ Confirmed'),
        ('completed', '🎉 Completed'),
        ('cancelled', '❌ Cancelled'),
    )

    consumer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    listing = models.ForeignKey(EnergyListing, on_delete=models.CASCADE, related_name='orders')
    quantity_kwh = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=50, blank=True)
    transaction_id = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.id} - {self.consumer.username}"

    def save(self, *args, **kwargs):
        if not self.total_amount:
            self.total_amount = self.quantity_kwh * self.listing.price_per_kwh
        super().save(*args, **kwargs)


class Transaction(models.Model):
    """Transaction record"""
    TRANSACTION_TYPES = (
        ('purchase', '🛒 Purchase'),
        ('sale', '💰 Sale'),
        ('refund', '↩️ Refund'),
    )

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='transaction')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions_sent')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions_received')
    payment_gateway = models.CharField(max_length=50, blank=True)
    gateway_transaction_id = models.CharField(max_length=200, blank=True)
    is_successful = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Transaction #{self.id} - ₹{self.amount}"