from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Plan, Subscription

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ['id', 'name', 'price', 'duration_days', 'created_at', 'updated_at']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class SubscriptionSerializer(serializers.ModelSerializer):
    plan = PlanSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    plan_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Subscription
        fields = [
            'id', 'user', 'plan', 'plan_id', 'start_date', 
            'end_date', 'status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'start_date', 'end_date', 'created_at', 'updated_at']

    def validate_plan_id(self, value):
        try:
            Plan.objects.get(id=value)
        except Plan.DoesNotExist:
            raise serializers.ValidationError("Plan does not exist.")
        return value

class SubscriptionCreateSerializer(serializers.ModelSerializer):
    plan_id = serializers.IntegerField()

    class Meta:
        model = Subscription
        fields = ['plan_id']

    def validate_plan_id(self, value):
        try:
            plan = Plan.objects.get(id=value)
        except Plan.DoesNotExist:
            raise serializers.ValidationError("Plan does not exist.")
        
        # Check if user already has active subscription to this plan
        user = self.context['request'].user
        existing = Subscription.objects.filter(
            user=user, 
            plan=plan, 
            status='active'
        ).exists()
        
        if existing:
            raise serializers.ValidationError("You already have an active subscription to this plan.")
        
        return value

