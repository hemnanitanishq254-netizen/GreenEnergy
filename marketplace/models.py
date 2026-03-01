from django.db import models
from django.core.validators import MinValueValidator
from accounts.models import User


class EnergyListing(models.Model):
    """Energy available for sale"""
    STATUS_CHOICES = (
        ('active', '✅ Active'),
        ('sold', '❌ Sold'),
        ('expired', '⏰ Expired'),
    )

    producer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    title = models.CharField(max_length=200)
    energy_type = models.CharField(max_length=20)
    quantity_kwh = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    price_per_kwh = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0)])
    available_from = models.DateField()
    available_until = models.DateField()
    description = models.TextField()
    location = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.quantity_kwh} kWh"

    @property
    def total_value(self):
        return self.quantity_kwh * self.price_per_kwh