from django.db import models
from account.models import *
# Create your models here.

class PaymentRequest(models.Model):
    STATUS = (
        
        ('Accepted','Accepted'),
        ('Completed','Completed'),
        ('Cancelled','Cancelled'),
       
    )
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    upi_id=models.CharField(max_length=25)
    amount=models.DecimalField(max_digits=6,decimal_places=2)
    created_at=models.DateTimeField(auto_now_add=True)
    status  =   models.CharField(max_length=10,choices=STATUS,default='Requested')
    def __str__(self):
        return f'PaymentRequest: {self.user.username}, Amount: {self.amount}'