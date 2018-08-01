from abc import ABC, abstractmethod


class AbstractCurrencyExchange(ABC):

    @abstractmethod
    def latest_exchange_rate(self, symbols):
        raise NotImplementedError()

    @abstractmethod
    def rates_for_day(self, day, symbols):
        raise NotImplementedError()


__all__ = ['AbstractCurrencyExchange']