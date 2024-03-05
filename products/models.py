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
