from celery import shared_task
from .services import ExchangeRateService
import logging
import requests

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def fetch_exchange_rates(self):

    try:
        logger.info("Starting exchange rate fetch task")
        service = ExchangeRateService()
        rate_data = service.get_exchange_rate('USD', 'BDT')

        if not rate_data:
            logger.warning("No rate data returned from service")
            raise ValueError("Exchange rate service returned empty data")

        logger.info(
            f"Successfully fetched USD to BDT rate: {rate_data['rate']} "
            f"(Source: {rate_data['source']}, Fetched: {rate_data['fetched_at']})"
        )

        return {
            'base_currency': rate_data['base_currency'],
            'target_currency': rate_data['target_currency'],
            'rate': rate_data['rate'],
            'timestamp': rate_data['fetched_at'].isoformat(),
            'source': rate_data['source']
        }

    except requests.exceptions.RequestException as exc:
        logger.error(f"API request failed: {str(exc)}")
        self.retry(exc=exc, countdown=min(60 * (self.request.retries + 1), 300))
    except ValueError as exc:
        logger.error(f"Data validation error: {str(exc)}")
        self.retry(exc=exc)
    except Exception as exc:
        logger.critical(f"Unexpected error in exchange rate task: {str(exc)}")
        self.retry(exc=exc)
