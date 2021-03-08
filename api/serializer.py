from rest_framework import serializers
from .models import Transaction, Period, Transaction, Spending


class PeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Period
        fields = ('id', 'period_date', 'completed')


class SpendingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spending
        fields = ('id', 'name', 'enabled')


class TransactionSerializer(serializers.ModelSerializer):
    period = PeriodSerializer(read_only=True)
    spending = SpendingSerializer(read_only=True)

    class Meta:
        model = Transaction
        fields = ('id', 'item', 'price', 'spending', 'period')
