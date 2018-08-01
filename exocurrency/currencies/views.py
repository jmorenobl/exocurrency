from dateutil.parser import parse

from django.utils.timezone import datetime

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status

from .models import Currency, CurrencyRate
from .api.serializers import CurrencyRateSerializer


class CurrencyRateListAPIView(ListAPIView):
    queryset = CurrencyRate.historical.all()
    serializer_class = CurrencyRateSerializer

    def get(self, request):
        from_day = parse(request.GET.get('fromDay'))
        to_day = parse(request.GET.get('toDay'))

        qs = self.get_queryset()
        qs = qs.between_dates(from_date=from_day, to_date=to_day)
        
        cls = self.get_serializer_class()
        serialized = cls(qs, many=True)

        return Response(data=serialized.data)


class CurrencyExchangeAPIView(APIView):
    queryset = Currency.objects.all()

    def get(self, request, base, target, amount):
        currency_base = self.queryset.get(code=base) 
        rate = currency_base.to_currency(target)

        target_amount = rate * amount

        data = {
            'base': base,
            'target': target,
            'base_amount': amount,
            'target_amount': target_amount
        }

        return Response(data=data)


class TimeWeightedRateReturnAPIView(APIView):
    queryset = Currency.objects.all()

    def get(self, request, base, target, amount):
        from_day = parse(request.GET.get('fromDay'))

        twrr = CurrencyRate.historical.time_weighted_rate_of_return(from_day, base, target, amount)

        return Response(data={'value': twrr})