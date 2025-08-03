from rest_framework import generics, status, views
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.db import transaction
from django.utils import timezone
from django.shortcuts import get_object_or_404
from .models import Plan, Subscription
from ..core.response import success_response, failure_response
from .serializers import (
    PlanSerializer, SubscriptionSerializer,
    SubscriptionCreateSerializer
)
import logging
from ..core.pagination import CustomPagination

logger = logging.getLogger(__name__)


class PlanCreateAPIView(generics.CreateAPIView):
    serializer_class = PlanSerializer
    permission_classes = [IsAdminUser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            try:
                with transaction.atomic():
                    plan = Plan.objects.create(**serializer.validated_data)
                    response_serializer = PlanSerializer(plan)
                    return success_response(
                        "Plan created successfully",
                        response_serializer.data,
                        status=status.HTTP_201_CREATED
                    )

            except Exception as e:
                logger.error(e)
                return failure_response("Error creating plan", status=status.HTTP_400_BAD_REQUEST)

        return failure_response("Invalid data", serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PlanListAPIView(generics.ListAPIView):
    queryset = Plan.objects.all().order_by('-created_at')
    serializer_class = PlanSerializer
    pagination_class = None


class SubscriptionCreateAPIView(generics.CreateAPIView):
    serializer_class = SubscriptionCreateSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            try:
                with transaction.atomic():
                    plan = get_object_or_404(
                        Plan, id=serializer.validated_data['plan_id'])

                    subscription = Subscription.objects.create(
                        user=request.user,
                        plan=plan,
                        start_date=timezone.now()
                    )

                    response_serializer = SubscriptionSerializer(subscription)
                    return success_response(
                        "Subscription created successfully",
                        response_serializer.data,
                        status=status.HTTP_201_CREATED
                    )

            except Exception as e:
                logger.error(f"Error creating subscription: {str(e)}")
                return failure_response("Error creating subscription", {}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return failure_response("Invalid data", serializer.errors)


class UserSubscriptionListAPIView(generics.ListAPIView):
    """
    List all subscriptions 
    """
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        return Subscription.objects.filter(
            user=self.request.user
        ).select_related('plan', 'user').order_by('-created_at')


class SubscriptionDetailAPIView(generics.RetrieveAPIView):
    """
    Retrieve a specific subscription 
    """
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Subscription.objects.filter(
            user=self.request.user
        ).select_related('plan', 'user')


class SubscriptionCancelAPIView(views.APIView):
    """
    Cancel a user's active subscription
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, subscription_id, *args, **kwargs):
        if not subscription_id:
            return Response({
                'success': False,
                'message': 'subscription_id is required'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                subscription = get_object_or_404(
                    Subscription,
                    id=subscription_id,
                    user=request.user,
                    status='active'
                )

                subscription.status = 'cancelled'
                subscription.save()

                return success_response(
                    "Subscription cancelled successfully",
                    SubscriptionSerializer(subscription).data,
                    status=status.HTTP_200_OK
                )

        except Exception as e:
            logger.error(f"Error cancelling subscription: {str(e)}")
            return failure_response("Error cancelling subscription", {}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AllSubscriptionsAPIView(generics.ListAPIView):
    """
    list all subscriptions 
    """
    serializer_class = SubscriptionSerializer
    pagination_class =CustomPagination

    def get_queryset(self):
        return Subscription.objects.select_related(
            'user', 'plan'
        ).order_by('-created_at')

    def list(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return failure_response("Unauthorized or you have no permission", {}, status=status.HTTP_403_FORBIDDEN)

        return super().list(request, *args, **kwargs)
