from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CurrencyRateManager
from ..drivers import fixer


class Currency(models.Model):
    code = models.CharField(_('code'), max_length=3, unique=True)
    is_base = models.BooleanField(_('base'), default=False, 
        help_text=_('Make this the base currency against which rates are calculated.'))
    
    def __str__(self):
        return '{0}'.format(self.code)

    def to_currency(self, code):
        if self.code != 'EUR':
            raise NotImplementedError('Only supported for EURO as base currency')

        fce = fixer.FixerCurrencyExchange()
        response = fce.latest_exchange_rate([code])

        return response['rates'][code]


class CurrencyRate(models.Model):
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='rates')
    date = models.DateField()
    factor = models.DecimalField(_('factor'), max_digits=30, decimal_places=10, default=1.0, 
        help_text=_('Specifies the difference of the currency to base one.'))

    objects = models.Manager()
    historical = CurrencyRateManager()

    def __str__(self):
        return '{0}@{1}'.format(self.currency, self.date.strftime('%Y-%m-%d'))
