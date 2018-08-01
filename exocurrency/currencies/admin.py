from django.contrib import admin

from .models import Currency, CurrencyRate


# Register your models here.
@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    pass


@admin.register(CurrencyRate)
class CurrencyRateAdmin(admin.ModelAdmin):
    pass
