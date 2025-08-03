from ..core.response import success_response, failure_response
from .services import ExchangeRateService
from rest_framework import generics, status, views
from ..core.pagination import CustomPagination
from .models import ExchangeRateLog
from .serializers import ExchangeRateSerializer


import logging

logger = logging.getLogger(__name__)


class ExchangeRateAPIView(views.APIView):
    """
    Get exchange rate between two currencies
    """

    def get(self, request, *args, **kwargs):
        base = request.query_params.get('base', 'USD')
        target = request.query_params.get('target', 'BDT')

        if not base or not target:
            return failure_response("Both base and target currencies are required", {})
        try:
            service = ExchangeRateService()
            rate_data = service.get_exchange_rate(base, target)

            if rate_data:
                return success_response("Exchange rate fetched", rate_data)
            else:
                return failure_response("Failed to fetch exchange rate", {})

        except Exception as e:
            logger.error(f"Error fetching exchange rate: {str(e)}")
            return failure_response('An error occurred while fetching exchange rate',{}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ExchangeRateHistoryAPIView(generics.ListAPIView):
    """
    List exchange rate history
    """
    serializer_class = ExchangeRateSerializer
    pagination_class= CustomPagination
    def get_queryset(self):
        base = self.request.query_params.get('base', 'USD')
        target = self.request.query_params.get('target', 'BDT')

        queryset = ExchangeRateLog.objects.filter(
            base_currency=base,
            target_currency=target
        ).order_by('-fetched_at')

        return queryset
