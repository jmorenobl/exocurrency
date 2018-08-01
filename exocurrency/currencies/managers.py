from django.db import models
from django.utils.timezone import datetime


class HistoricalRatesQuerySet(models.QuerySet):
    def between_dates(self, from_date, to_date):
        return self.filter(date__gte=from_date, date__lt=to_date)


class CurrencyRateManager(models.Manager):

    def get_queryset(self):
        return HistoricalRatesQuerySet(self.model, using=self._db)

    def between_dates(self, from_date, to_date):
        return self.get_queryset().between_dates(from_date, to_date)

    def time_weighted_rate_of_return(self, from_date, base, target, amount):
        if 'EUR' != base:
            raise NotImplementedError('Currency base other than EURO is not currently supported')

        to_date = datetime.today().date()
        rates = self.between_dates(from_date, to_date).select_related('currency').filter(currency__code=target)

        beginning_market_value = rates[0].factor * amount
        twr = 1
        for rate in rates:
            ending_market_value = rate.factor * amount
            rn = ((ending_market_value - beginning_market_value)/beginning_market_value) * 100
            twr *= 1 + rn
            
            # For the next iteration
            beginning_market_value = ending_market_value

        twr = twr - 1

        return twr
