import requests

from django.conf import settings

from ..base import AbstractCurrencyExchange


class FixerCurrencyExchange(AbstractCurrencyExchange):

    def __init__(self, *args, **kwargs):
        self.base_url = 'http://data.fixer.io/api/{}'

    def request(self, endpoint, payload):
        response = requests.get(endpoint, params=payload)
        data = response.json()

        return {
            'base': data['base'],
            'date': data['date'],
            'rates': data['rates']
        }

    def latest_exchange_rate(self, symbols):
        """latest endpoint - request the most recent exchange rate data"""

        endpoint = self.base_url.format('latest')
        payload = {
            'access_key': settings.FIXER_ACCESS_KEY,
            'symbols': ",".join(symbols)
        }
        
        return self.request(endpoint, payload)

    
    def rates_for_day(self, day, symbols):
        """historical endpoint - request historical rates for a specific day"""

        endpoint = self.base_url.format(day.strftime('%Y-%m-%d'))
        payload = {
            'access_key': settings.FIXER_ACCESS_KEY,
            'symbols': ",".join(symbols)
        }

        return self.request(endpoint, payload)


__all__ = ['FixerCurrencyExchange']