from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from ..core.models import TimeStampedModel

class Plan(TimeStampedModel):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price in USD")
    duration_days = models.PositiveIntegerField(help_text="Duration in days")

    def __str__(self):
        return f"{self.name} - ${self.price} for {self.duration_days} days"

    class Meta:
        ordering = ['price']
        verbose_name_plural = "Subscriptions Plan "

class Subscription(TimeStampedModel):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('cancelled', 'Cancelled'),
        ('expired', 'Expired'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')


    def save(self, *args, **kwargs):
        if not self.end_date:
            self.end_date = self.start_date + timedelta(days=self.plan.duration_days)
        
        # Auto-expire if past end date
        if timezone.now() > self.end_date and self.status == 'active':
            self.status = 'expired'
            
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} bought a subscription to {self.plan.name} ({self.status})"

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "User Subscriptions"

