from django.test import TestCase
from .services import ExchangeRateService

class ExchangeRateServiceTest(TestCase):
    def test_exchange_rate_service(self):
        service = ExchangeRateService()
        self.assertIsInstance(service, ExchangeRateService)
