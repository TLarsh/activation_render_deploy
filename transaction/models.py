from django.db import models
import uuid

from authenticate.models import User

# Create your models here.
class Transaction(models.Model):
    TRANSACTION_OPTION = [
        ('DEPOSITE','DEPOSITE'),
        ('TRANSFER','TRANSFER')
    ]
    user = models.ForeignKey(User ,on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    account_number = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
    action = models.CharField(choices=TRANSACTION_OPTION, max_length=50, default='D')
    transaction_id = models.UUIDField(default =uuid.uuid4)
    status = models.CharField(max_length=50, default='Failure')