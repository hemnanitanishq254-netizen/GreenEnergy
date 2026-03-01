from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator


class User(AbstractUser):
    """Extended User Model with roles"""
    USER_ROLES = (
        ('producer', 'Energy Producer'),
        ('consumer', 'Energy Consumer'),
        ('investor', 'Investor'),
    )

    role = models.CharField(max_length=20, choices=USER_ROLES, default='consumer')
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    pincode = models.CharField(max_length=10, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class ProducerProfile(models.Model):
    """Producer specific details"""
    ENERGY_TYPES = (
        ('solar', '☀️ Solar Energy'),
        ('wind', '💨 Wind Energy'),
        ('biogas', '🌿 Biogas'),
        ('hydro', '💧 Hydroelectric'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='producer_profile')
    energy_type = models.CharField(max_length=20, choices=ENERGY_TYPES)
    capacity_kw = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    installation_date = models.DateField()
    certification_number = models.CharField(max_length=100, blank=True)
    certification_doc = models.FileField(upload_to='certifications/', blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_energy_type_display()}"


class ConsumerProfile(models.Model):
    """Consumer specific details"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='consumer_profile')
    monthly_consumption_kwh = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    preferred_energy_type = models.CharField(max_length=20, choices=ProducerProfile.ENERGY_TYPES, blank=True)
    budget_per_month = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - Consumer"


class InvestorProfile(models.Model):
    """Investor specific details"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='investor_profile')
    company_name = models.CharField(max_length=200, blank=True)
    investment_capacity = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    pan_number = models.CharField(max_length=10, blank=True)
    preferred_sectors = models.TextField(help_text="Comma-separated: solar, wind, biogas")

    def __str__(self):
        return f"{self.user.username} - Investor"


from django.db import models

# Create your models here.
