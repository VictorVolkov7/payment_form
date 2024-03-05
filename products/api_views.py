import os

import stripe
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView

from products.models import Item


class ItemDetailIView(APIView):
    """
    Retrieves html page a single item from the database.
    """

    @staticmethod
    def get(request, *args, **kwargs):
        item = get_object_or_404(Item, pk=kwargs.get('pk'))
        return render(request, 'item_detail.html', {'object': item})


class StripeSessionDetail(APIView):
    """
    Retrieves stripe's session id.
    """
    stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

    @staticmethod
    def get(request, *args, **kwargs):
        item = get_object_or_404(Item, pk=kwargs.get('pk'))

        item_name = item.name
        item_price = item.price * 100

        session = stripe.checkout.Session.create(
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': item_name,
                    },
                    "unit_amount_decimal": item_price
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='http://localhost:8000/success',
            cancel_url='http://localhost:8000/cancel',
        )

        return JsonResponse({'session_id': session.id})
