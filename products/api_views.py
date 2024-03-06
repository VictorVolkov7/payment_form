import os

import stripe
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView

from products.models import Item, Order


class ItemDetailIView(APIView):
    """
    Retrieves html page a single item from the database.
    """

    @staticmethod
    def get(request, *args, **kwargs):
        item = get_object_or_404(Item, pk=kwargs.get('pk'))
        return render(request, 'item_detail.html', {'object': item})


class OrderDetailIView(APIView):
    """
    Retrieves html page order from the database.
    """

    @staticmethod
    def get(request, *args, **kwargs):
        order = get_object_or_404(Order, pk=kwargs.get('pk'))
        order.calculate_total_price()
        order.name = f'Order {order.pk}'
        order.save()
        return render(request, 'order_detail.html', {'object': order})


class StripeSessionDetail(APIView):
    """
    Retrieves stripe's session id.
    """
    stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

    @staticmethod
    def get(request, *args, **kwargs):
        if 'order' in request.path:
            order = get_object_or_404(Order, pk=kwargs.get('pk'))
            stripe_name = order.name
            stripe_price = order.total_price * 100
        else:
            item = get_object_or_404(Item, pk=kwargs.get('pk'))
            stripe_name = item.name
            stripe_price = item.price * 100

        session = stripe.checkout.Session.create(
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': stripe_name,
                    },
                    "unit_amount_decimal": stripe_price
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='http://localhost:8000/success',
            cancel_url='http://localhost:8000/cancel',
        )

        return JsonResponse({'session_id': session.id})
