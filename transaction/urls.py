from django.urls import path

from transaction.views import(
    TransactionHistoryAPIView,
    DepositeAPIView,
    TransferAPIView
)

urlpatterns = [
    path('deposite/', DepositeAPIView.as_view(), name='deposite'),
    path('transfer/', TransferAPIView.as_view(), name='transfer'),
    path('transaction-history/', TransactionHistoryAPIView.as_view(), name='transact-history')
]