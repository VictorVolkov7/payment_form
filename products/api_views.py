import os

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView

from products.models import Item, Order
from products.services import stipe_payment_created


@extend_schema(
    summary="Retrieves simple html page with item.",
    )
class ItemDetailIView(APIView):
    """
    Retrieves html page a single item from the database.
    """

    @staticmethod
    def get(request, *args, **kwargs):
        item = get_object_or_404(Item, pk=kwargs.get('pk'))
        return render(
            request, 'item_detail.html', {'object': item, 'api_key': os.getenv('STRIPE_PUBLIC_KEY')}
        )


@extend_schema(
    summary="Retrieves simple html page with order.",
    )
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
        return render(
            request, 'order_detail.html', {'object': order, 'api_key': os.getenv('STRIPE_PUBLIC_KEY')}
        )


@extend_schema(
    summary=" Retrieves stripe's session id.",
    )
class StripeSessionDetail(APIView):
    """
    Retrieves stripe's session id.
    """
    @staticmethod
    def get(request, *args, **kwargs):
        if 'order' in request.path:
            order = get_object_or_404(Order, pk=kwargs.get('pk'))
            stripe_price = order.total_price * 100
            session = stipe_payment_created(order, stripe_price)
        else:
            item = get_object_or_404(Item, pk=kwargs.get('pk'))
            stripe_price = item.price * 100
            session = stipe_payment_created(item, stripe_price)

        return JsonResponse({'session_id': session.id})
