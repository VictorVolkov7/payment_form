from django.db import models
from django.utils.translation import gettext_lazy as _


class Item(models.Model):
    """
    Item model.
    """

    name = models.CharField(
        max_length=150,
        verbose_name=_('Name')
    )
    description = models.TextField(
        verbose_name=_('Description')
    )
    price = models.DecimalField(
        max_digits=19,
        decimal_places=2,
        verbose_name=_('Price')
    )

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = _('Item')
        verbose_name_plural = _('Items')


class Discount(models.Model):
    """
    Discount model.
    """
    discount = models.SmallIntegerField(verbose_name=_('Discount'), default=0)

    def __str__(self):
        return f'{self.discount} %'

    class Meta:
        verbose_name = _('Discount')
        verbose_name_plural = _('Discounts')


class Order(models.Model):
    """
    Order model.
    """
    name = models.CharField(
        max_length=30,
        default=_('New order'),
        blank=True,
        null=True,
        verbose_name=_('Name'),
    )
    items = models.ManyToManyField(
        Item,
        related_name='items',
        verbose_name=_('Items'),
    )
    total_price = models.DecimalField(
        max_digits=19,
        decimal_places=2,
        default=0.0,
        verbose_name=_('Total Price'),
    )
    discount = models.ForeignKey(
        Discount,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Discount')
    )

    def calculate_total_price(self):
        """
        Calculate total item's price.
        """
        total = sum(item.price for item in self.items.all())
        self.total_price = total
        self.save()

    def __str__(self):
        return f'{self.name} - {self.total_price}'

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')
