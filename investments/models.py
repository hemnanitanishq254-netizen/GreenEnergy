from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import User


class InvestmentProject(models.Model):
    """Renewable energy investment project"""
    STATUS_CHOICES = (
        ('planning', '📋 Planning'),
        ('funding', '💰 Seeking Funding'),
        ('active', '🚀 Active'),
        ('completed', '✅ Completed'),
    )

    ENERGY_TYPES = (
        ('solar', '☀️ Solar'),
        ('wind', '💨 Wind'),
        ('biogas', '🌿 Biogas'),
        ('hydro', '💧 Hydro'),
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    energy_type = models.CharField(max_length=20, choices=ENERGY_TYPES)
    location = models.CharField(max_length=200)
    total_funding_required = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    funding_raised = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    expected_roi_percent = models.DecimalField(max_digits=5, decimal_places=2,
                                               validators=[MinValueValidator(0), MaxValueValidator(100)])
    project_duration_months = models.IntegerField(validators=[MinValueValidator(1)])
    capacity_kw = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planning')
    start_date = models.DateField(null=True, blank=True)
    expected_completion = models.DateField()
    project_document = models.FileField(upload_to='projects/', blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_projects')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.get_energy_type_display()}"

    @property
    def funding_progress(self):
        if self.total_funding_required > 0:
            return (self.funding_raised / self.total_funding_required) * 100
        return 0


class Investment(models.Model):
    """Individual investment in a project"""
    STATUS_CHOICES = (
        ('active', '✅ Active'),
        ('completed', '🎉 Completed'),
        ('withdrawn', '↩️ Withdrawn'),
    )

    project = models.ForeignKey(InvestmentProject, on_delete=models.CASCADE, related_name='investments')
    investor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='investments')
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    investment_date = models.DateField(auto_now_add=True)
    expected_return = models.DecimalField(max_digits=12, decimal_places=2)
    actual_return = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.investor.username} - ₹{self.amount} in {self.project.title}"

    def save(self, *args, **kwargs):
        if not self.expected_return:
            roi = float(self.project.expected_roi_percent) / 100
            self.expected_return = float(self.amount) * (1 + roi)
        super().save(*args, **kwargs)