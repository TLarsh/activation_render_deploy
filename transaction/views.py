from django.http import HttpResponse
from django.shortcuts import render

from transaction.models import Transaction
from .serializers import TransactionSerilizer, TransferSerilizer
from rest_framework import generics, response, status, permissions
from authenticate.models import User


# Create your views here.

class DepositeAPIView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    
    serializer_class = TransactionSerilizer
    def perform_create(self,serializer):
        user = self.request.user
        amount = serializer.validated_data['amount']
        account_number = user.account_number
        action = serializer.validated_data['action']
        recipient = User.objects.get(account_number=account_number)
        user.balance += amount
        user.save()
        status = 'Successful'
        Transaction.objects.create(amount=amount, user=user, action=action, account_number=account_number, status=status)
        return response.Response(recipient.username)
    
class TransferAPIView(generics.CreateAPIView):
    serializer_class = TransferSerilizer
    def perform_create(self, serializer):
        user = self.request.user
        amount = serializer.validated_data['amount']
        account_number = serializer.validated_data['account_number']
        action = serializer.validated_data['action']
        recipient = User.objects.get(account_number=account_number)
        serializer.is_valid(raise_exception=True)
        user.balance -= amount
        user.save()
        recipient.balance += amount
        recipient.save()
        status = 'Successful'
        Transaction.objects.create(amount=amount, user=user, action=action, account_number=account_number, status=status)

    
        
class TransactionHistoryAPIView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = TransactionSerilizer
    def get_queryset(self):
        user = self.request.user
        return Transaction.objects.filter(user=user)
    
        

