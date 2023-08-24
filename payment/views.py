import json
import razorpay
import datetime
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import *
from .serializers import *
from django.utils import timezone
import requests
from rest_framework.permissions import IsAuthenticated
from backend.settings import RAZOR_KEY_ID,RAZOR_KEY_SECRET
from account.models import CustomUser
from rest_framework.decorators import api_view,permission_classes,APIView
from rest_framework.response import Response
from recipe.models import Notifications
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
# Create your views here.

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def start_payment(request):

    amount=10000
    client =  razorpay.Client(auth=(RAZOR_KEY_ID,RAZOR_KEY_SECRET))
    payment = client.order.create({"amount": amount, 
                                   "currency": "INR"
                                   })
    data = {
        "payment": payment
    }
    return Response(data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def handle_payment_success(request):
    try:

            user=request.user
            res = json.loads(request.data["response"])
            
            ord_id = ""
            raz_pay_id = ""
            raz_signature = ""
            for key in res.keys():
                if key == 'razorpay_order_id':
                    ord_id = res[key]
                elif key == 'razorpay_payment_id':
                    raz_pay_id = res[key]
                elif key == 'razorpay_signature':
                    raz_signature = res[key]

            data = {
                'razorpay_order_id': ord_id,
                'razorpay_payment_id': raz_pay_id,
                'razorpay_signature': raz_signature
            }

            client =  razorpay.Client(auth=(RAZOR_KEY_ID,RAZOR_KEY_SECRET))
            
        
            check = client.utility.verify_payment_signature(data)
            

            if not check:
                    print("Redirect to error url or error page")
                    return Response({'error': 'Something went wrong'})
            try:

            
                user.has_premium = True

                user.premium_expiry = timezone.now() + timezone.timedelta(days=30)             
                user.save()
                transaction_details={
                     'transaction_id':ord_id,
                     'amount':100,
                     'time':timezone.now().isoformat(),
                     'type':'premium'
                }
                user.add_transaction(transaction_details)
               
                return Response({'message':"User is now a premium subscriber",'status':200,})
            except Exception as e:
                return Response({'message':"Error updating user premium status:",'error': str(e),'status':400})
    except Exception as e:
         return Response({'error':str(e)})
            
            

class PaymentRequest(APIView):
        authentication_classes = [JWTAuthentication]
        permission_classes = [IsAuthenticated]

        def post(self,request):
             data=request.data
            #  upi_id=data['upi_id']
             amount = data['amount']
             user_id=request.user.id
             user=CustomUser.objects.get(pk=user_id)
             serializer=PaymentRequestSerializer(data=data)
             if serializer.is_valid():
                    serializer.save()
                    notification_message=f"{user.username} has requested a payment of amount:{amount}"
                    admin_user=CustomUser.objects.filter(is_superuser=True).first()
                    Notifications.objects.create(sender=user,recipient=admin_user,message=notification_message,is_read=False)
                    
                    channel_layer=get_channel_layer()
                    author_channel_name=f"user_{admin_user.id}"
                    print(author_channel_name)
                    async_to_sync(channel_layer.group_send)(
                            author_channel_name,
                            {
                                "type":"send_notification",
                                "notification":{
                                    "message":notification_message,
                                    "is_read":False,
                                },
                            },
                    )
                    return Response({'message':'Your request is accepted.Amount will be credited in 3-4 days','status':200})
             return Response({'error':serializer.errors,'status':400})
             

