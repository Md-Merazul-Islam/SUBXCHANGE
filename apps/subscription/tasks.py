from celery import shared_task
from django.utils import timezone
from .models import Subscription
import logging

logger = logging.getLogger(__name__)

@shared_task
def update_expired_subscriptions():
    """
    Task to update expired subscriptions
    """
    try:
        expired_count = Subscription.objects.filter(
            status='active',
            end_date__lt=timezone.now()
        ).update(status='expired')
        
        logger.info(f"Updated {expired_count} expired subscriptions")
        return f"Updated {expired_count} expired subscriptions"
        
    except Exception as e:
        logger.error(f"Error in update_expired_subscriptions task: {str(e)}")
        return f"Error: {str(e)}"

@shared_task
def cleanup_old_exchange_logs():
    """
    Clean up exchange rate logs older than 30 days
    """
    try:
        from ..subscription.models import ExchangeRateLog
        cutoff_date = timezone.now() - timezone.timedelta(days=30)
        
        deleted_count = ExchangeRateLog.objects.filter(
            fetched_at__lt=cutoff_date
        ).delete()[0]
        
        logger.info(f"Cleaned up {deleted_count} old exchange rate logs")
        return f"Cleaned up {deleted_count} old exchange rate logs"
        
    except Exception as e:
        logger.error(f"Error in cleanup_old_exchange_logs task: {str(e)}")
        return f"Error: {str(e)}"