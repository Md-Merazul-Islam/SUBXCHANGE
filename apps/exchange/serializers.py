from rest_framework import serializers
from .models import ExchangeRateLog

class ExchangeRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeRateLog
        fields = ['base_currency', 'target_currency', 'rate', 'fetched_at']