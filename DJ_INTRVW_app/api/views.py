from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse

from django.views import View
from django.views.generic import TemplateView, ListView

from .models import Item

import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.

class ItemsListView(ListView):
    model = Item
    template_name = "items.html"

class ItemPageView(TemplateView):
    template_name = "item.html"

    def get_context_data(self, **kwargs):
        item = Item.objects.get(id=self.kwargs['pk'])
        context = super(ItemPageView, self).get_context_data(**kwargs)
        context.update({
            "item": item,
            "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY
        })
        return context

class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        item_id = self.kwargs["pk"]
        item = Item.objects.get(id=item_id)

        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price_data': {
                        'currency': 'kzt',
                        'product_data': {
                            'name': item.name,
                            'description': item.description,
                        },
                        'unit_amount_decimal': item.price,
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url="http://127.0.0.1:8000" + '/success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url="http://127.0.0.1:8000" + '/cancel',
        )
        return JsonResponse({
            'id': checkout_session.id
        })

class SuccessView(TemplateView):
    template_name = "success.html"

    def get_context_data(self, **kwargs):
        session_id = self.request.GET.get('session_id')
        context = super().get_context_data(**kwargs)
        context.update({
            "SESSION_ID": session_id
        })
        return context

class CancelView(TemplateView):
    template_name = "cancel.html"