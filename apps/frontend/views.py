from django.views.generic import ListView
from ..subscription.models import Subscription, Plan
from django.views.generic import TemplateView
from ..exchange.models import ExchangeRateLog


class SubscriptionListView(ListView):
    """
    Display all user subscriptions in a table format
    """
    model = Subscription
    template_name = 'subscriptions/sub_list.html'
    context_object_name = 'subscriptions'

    def get_queryset(self):
        return Subscription.objects.select_related(
            'user', 'plan'
        ).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['stats'] = {
            'total_subscriptions': Subscription.objects.count(),
            'active_subscriptions': Subscription.objects.filter(status='active').count(),
            'cancelled_subscriptions': Subscription.objects.filter(status='cancelled').count(),
            'expired_subscriptions': Subscription.objects.filter(status='expired').count(),
        }

        return context


class PlanListView(ListView):
    """
    Display all available plans
    """
    model = Plan
    template_name = 'plans/list.html'
    context_object_name = 'plans'

    def get_queryset(self):
        return Plan.objects.all().order_by('price')



class ExchangeRateView(TemplateView):
    template_name = 'exchg/exchg.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        base = self.request.GET.get('base', 'USD').upper()
        target = self.request.GET.get('target', 'BDT').upper()
        current_rate = ExchangeRateLog.objects.filter(
            base_currency=base,
            target_currency=target
        ).order_by('-fetched_at').first()
        
        history = ExchangeRateLog.objects.filter(
            base_currency=base,
            target_currency=target
        ).order_by('-fetched_at')

        context.update({
            'current_rate': current_rate,
            'selected_base': base,
            'history': history,
            'selected_target': target,
        })
        return context