from rest_framework import serializers
from .models import Transaction
import uuid

class TransactionSerilizer(serializers.ModelSerializer):
    user = serializers.CharField(max_length=50,min_length=3,read_only=True)
    account_number = serializers.CharField(max_length=50, read_only=True)
    status = serializers.CharField(max_length=50, read_only=True)
    
    class Meta:
        model = Transaction
        fields = ['user', 'amount', 'timestamp', 'transaction_id', 'action', 'account_number', 'status']


class TransferSerilizer(serializers.ModelSerializer):
    user = serializers.CharField(max_length=50,min_length=3,read_only=True)
    
    class Meta:
        model = Transaction
        fields = ['user', 'amount', 'timestamp', 'transaction_id', 'action', 'account_number']
    def validate(self, attrs):
        user = self.context['request'].user
        amount = attrs.get('amount')
        if user.balance <= amount:
            raise serializers.ValidationError('Insefficient Balance')
        return attrs