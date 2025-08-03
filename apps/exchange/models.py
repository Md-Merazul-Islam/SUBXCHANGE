from django.db import models

class ExchangeRateLog(models.Model):
    base_currency = models.CharField(max_length=3, default='USD')
    target_currency = models.CharField(max_length=3)
    rate = models.DecimalField(max_digits=15, decimal_places=6)
    fetched_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.base_currency} to {self.target_currency}: {self.rate} at {self.fetched_at}"

    class Meta:
        ordering = ['-fetched_at']
        unique_together = ['base_currency', 'target_currency', 'fetched_at']