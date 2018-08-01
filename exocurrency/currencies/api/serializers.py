from rest_framework import serializers

from ..models import Currency, CurrencyRate


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ('id', 'code', 'is_base')


class CurrencyRateSerializer(serializers.ModelSerializer):
    currency = serializers.StringRelatedField()

    class Meta:
        model = CurrencyRate
        fields = ('id', 'currency', 'date', 'factor')
