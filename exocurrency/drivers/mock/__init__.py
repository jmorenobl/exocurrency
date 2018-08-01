import random

from django.utils.timezone import datetime

from .base import AbstractCurrencyExchange


class MockCurrencyExchange(AbstractCurrencyExchange):

    def genarate_random_rates(self, symbols):
        random_rates = []

        for symbol in range(0, len(symbols)):
            random_rates.append(random.random() + 1)

        rates = dict(zip(symbols, random_rates))

        return rates

    def latest_exchange_rate(self, symbols):
        """latest endpoint - request the most recent exchange rate data"""
        
        rates = self.genarate_random_rates(symbols)

        return {
            'base': 'EUR',
            'date': datetime.today().strftime('%Y-%m-%d'),
            'rates': rates
        }

    
    def rates_for_day(self, day, symbols):
        """historical endpoint - request historical rates for a specific day"""

        rates = self.genarate_random_rates(symbols)

        return {
            'base': 'EUR',
            'date': day.strftime('%Y-%m-%d'),
            'rates': rates
        }


__all__ = ['MockCurrencyExchange']