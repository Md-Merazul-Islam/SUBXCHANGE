import requests
from django.conf import settings
from django.utils import timezone
from .models import ExchangeRateLog
import logging
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)

class ExchangeRateService:
    def __init__(self):
        self.base_url = f"{settings.EXCHANGE_API_URL}/{settings.EXCHANGE_API_KEY}"
        self.session = requests.Session()
 
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("https://", adapter)
        
    def _make_api_request(self, endpoint):
        """Helper method to make API requests with proper headers"""
        try:
            response = self.session.get(
                f"{self.base_url}/{endpoint}",
                headers={'Accept': 'application/json'},
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"API request failed: {e.response.status_code} - {e.response.text}")
            if e.response.status_code == 429:
                logger.warning("Rate limit exceeded")
            return None
        except Exception as e:
            logger.error(f"Unexpected API error: {str(e)}")
            return None

    def get_exchange_rate(self, base_currency='USD', target_currency='BDT'):
        """
        Fetch exchange rate with proper API key usage and enhanced error handling
        """
        # Check cache first
        recent_rate = ExchangeRateLog.objects.filter(
            base_currency=base_currency,
            target_currency=target_currency,
            fetched_at__gte=timezone.now() - timezone.timedelta(hours=1)
        ).first()

        if recent_rate:
            return {
                'base_currency': recent_rate.base_currency,
                'target_currency': recent_rate.target_currency,
                'rate': float(recent_rate.rate),
                'fetched_at': recent_rate.fetched_at,
                'source': 'cache'
            }

        # Fetch from API
        data = self._make_api_request(f"latest/{base_currency}")
        if not data or 'conversion_rates' not in data:
            return None

        if target_currency in data['conversion_rates']:
            rate = data['conversion_rates'][target_currency]
            exchange_log = ExchangeRateLog.objects.create(
                base_currency=base_currency,
                target_currency=target_currency,
                rate=rate
            )

            return {
                'base_currency': base_currency,
                'target_currency': target_currency,
                'rate': float(rate),
                'fetched_at': exchange_log.fetched_at,
                'source': 'api'
            }
        
        logger.error(f"Currency {target_currency} not found in API response")
        return None

    def fetch_multiple_rates(self, base_currency='USD', target_currencies=None):
        """Fetch multiple rates with a single API call"""
        if target_currencies is None:
            target_currencies = ['BDT', 'EUR', 'GBP']
            
        data = self._make_api_request(f"latest/{base_currency}")
        if not data or 'conversion_rates' not in data:
            return []
            
        results = []
        for currency in target_currencies:
            if currency in data['conversion_rates']:
                rate = data['conversion_rates'][currency]
                ExchangeRateLog.objects.create(
                    base_currency=base_currency,
                    target_currency=currency,
                    rate=rate
                )
                results.append({
                    'base_currency': base_currency,
                    'target_currency': currency,
                    'rate': float(rate),
                    'fetched_at': timezone.now(),
                    'source': 'api'
                })
        
        return results