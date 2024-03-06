from django.urls import path

from products.api_views import ItemDetailIView, StripeSessionDetail, OrderDetailIView
from products.apps import ProductsConfig

app_name = ProductsConfig.name

urlpatterns = [
    path('item/<int:pk>/', ItemDetailIView.as_view(), name='item-detail'),
    path('order/<int:pk>/', OrderDetailIView.as_view(), name='order-detail'),
    path('buy/<int:pk>/', StripeSessionDetail.as_view(), name='item-buy'),
    path('buy/order/<int:pk>/', StripeSessionDetail.as_view(), name='order-buy'),
]
