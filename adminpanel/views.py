from django.shortcuts import render
from .serializers import *
from datetime import timedelta

from account.models import CustomUser
import datetime
from recipe.serializers import CategorySerializer,notificationAdminSerializer
from decimal import Decimal
from rest_framework.views import APIView
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.response import Response
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from .models import Categories
from payment.models import PaymentRequest
from django.db.models.functions import Trunc
from recipe.models import Recipe,Notifications
from rest_framework.pagination import PageNumberPagination
# Create your views here.


# Listing all the users
class MyPageNumberPagination(PageNumberPagination):
     page_size = 5  # Number of items per page

class UserList(generics.ListAPIView):
    # verifies authenticated using jwt
    authentication_classes = [JWTAuthentication]
    # verifies user is adminuser
    permission_classes = [IsAdminUser] 
    queryset=CustomUser.objects.filter(is_user=True).order_by('-id')
    serializer_class=UserSerializer
    pagination_class=MyPageNumberPagination


    # getting user list
    def get(self,request,user_id=None):
        try:
            if user_id is not None:
                    user =CustomUser.objects.get(pk=user_id)
                    
                    serializer=UserDetailSerializer(user)
                    return Response({'payload':serializer.data,'message':'success','status':200 })
            else:
                 return super().list(request)
        except CustomUser.DoesNotExist:
            return Response({'error':'User not found','status':404})
        except Exception as e:
            return Response({'error':e,'status':400})
        
    # for blocking and unblocking

    def patch(self,request):
        data=request.data
        try:
            user=CustomUser.objects.get(id=data['id'])
            username=user.username
            if data['status'] == True:
                user.is_block=False
                user.save()
                return Response({'message':f'{username} is Unblocked'})
            if data['status'] == False:
                user.is_block = True
                user.save()
                return Response({'message':f'{username} is Blocked'})    
        except Exception as e:
            return Response({'error':e})


class CategoryList(generics.ListAPIView):
    # verifies authenticated using jwt
    authentication_classes = [JWTAuthentication]
    # verifies user is adminuser
    permission_classes = [IsAdminUser] 

    queryset=Categories.objects.all().order_by('-id')
    serializer_class=CategorySerializer
    pagination_class=MyPageNumberPagination

                  
    def post(self,request):
        try:

            data=request.data
            print(data)
            serializer=CategorySerializer(data=request.data)
            print(serializer)
            if serializer.is_valid():
                serializer.save()
                return Response({'status':200,
                                    'message':'Category added successfully',
                                    'data':serializer.data})
            return Response({'status':400,
                                'message':'Category already exists',
                                'error':serializer.errors})
        except Exception as e:
            return Response({'error':e})

    def patch(self,request):
        data=request.data
        
        try:
            category=Categories.objects.get(id=data['id'])
            cat_name=category.name
            if data['status'] == True:
                category.is_disabled=False
                category.save()
                return Response({'message':f'{cat_name} is added back'})
            if data['status'] == False:
                category.is_disabled = True
                category.save()
            return Response({'status':200,'message':'Category disabled successfully'})
        except Exception as e:
            return({'error':e})

class ManageRequest(generics.ListAPIView):
    # verifies authenticated using jwt
    authentication_classes = [JWTAuthentication]
    # verifies user is adminuser
    permission_classes = [IsAdminUser]

    queryset=PaymentRequest.objects.all().order_by('-id')
    serializer_class=PaymentSerializer
    pagination_class=MyPageNumberPagination

        
    def post(self,request):
        try:
            data=request.data
            id=data['id']
            status=data['status']
            amount=data['amount']
            user=CustomUser.objects.get(pk=data['user'])
            payment_request = PaymentRequest.objects.get(pk=id)
            payment_request.status=status
            payment_request.save()
            yr  =   int(datetime.date.today().strftime('%Y'))
            dt  =   int(datetime.date.today().strftime('%d'))
            mt  =   int(datetime.date.today().strftime('%m'))
            d  =    datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d") #yyyy/mm/dd
            trans_id   =      current_date + data['user']
            
            transaction_details={
                'transaction_id':trans_id,
                'amount':amount,
                'time':timezone.now().isoformat(),
                'status':status,
                'type' :'earning'
            }
            user.add_transaction(transaction_details)
            if status == 'Completed':
                    
                    user.wallet=user.wallet-Decimal(amount)
                    user.save()
            
            return Response({'status':200,'message':'Status Updated Successfully'})
        except Exception as e:
            return Response({'error':str(e),'status':400})
        
        
class Recipes(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]  
    queryset=Recipe.objects.all().order_by('-total_reports')
    serializer_class=RecipeSerializer
    pagination_class=MyPageNumberPagination

    # def get(self,request):
    #     try:
    #         recipes=Recipe.objects.all().order_by('-total_reports')
    #         serializer=RecipeSerializer(recipes,many=True)
    #         return Response({'payload':serializer.data,'message':'success' })
    #     except Exception as e:
    #         return Response({'error':e})
    # def delete(self,request):
    #     pass
    # for blocking and unblocking

    def patch(self,request):
        data=request.data
        try:
            recipe=Recipe.objects.get(id=data['id'])
            recipe_name=recipe.recipe_name
            if data['status'] == True:
                recipe.is_disabled =False
                recipe.save()
                return Response({'message':f'{recipe_name} is Unblocked'})
            if data['status'] == False:
                recipe.is_disabled = True
                recipe.save()
                return Response({'message':f'{recipe_name} is Disabled'})    
        except Exception as e:
            return Response({'error':e})
        

# for graphs

class Analytics(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    def get(self,request):
        try:
        #    first set
           basic_users=CustomUser.objects.filter(is_active=True,has_premium=False).count()
           premium_users=CustomUser.objects.filter(is_active=True,has_premium=True).count()
           users_with_private = Recipe.objects.filter(is_private=True).values('author').distinct().count()
           other=premium_users-users_with_private
        #    2nd set
           recipe_types={}
           types=Categories.objects.all()
           for type in types:
               count=Recipe.objects.filter(category=type).count()
               recipe_types[type.name]=count
            # 3rd set
           transaction_history_queryset=CustomUser.objects.all().values('transaction_history')
           transaction_history = [json.loads(item['transaction_history']) for item in transaction_history_queryset]
           transactions=[]
           for signle_transaction_data in transaction_history :
               for transaction in signle_transaction_data:
                   transactions.append(transaction)
           accounts_daily={}
           for transaction in transactions:
                transaction_time = datetime.datetime.strptime(transaction['time'], '%Y-%m-%dT%H:%M:%S.%f%z')
                transaction_days = transaction_time.date()
                transaction_day = transaction_days.strftime("%d-%m-%Y")

               
                if transaction['type'] == 'earning':
                    accounts_daily.setdefault(transaction_day, {'income': 0, 'outgoing': 0})
                    accounts_daily[transaction_day]['outgoing'] += float(transaction['amount'])
                else:
                    accounts_daily.setdefault(transaction_day, {'income': 0, 'outgoing': 0})
                    accounts_daily[transaction_day]['income'] += float(transaction['amount'])
          
           

           data=[{'basic':basic_users,
               'premium':premium_users,
               'with_private':users_with_private,
               'without_private':other},
               {'category_recipe':recipe_types},
               {'transaction_details': accounts_daily}

           ]
           
           return Response({'payload':data,'status':200})

        except Exception as e:
            return Response({'error':str(e)})
# get latest notification
class Notification(APIView):
        authentication_classes = [JWTAuthentication]
        permission_classes = [IsAdminUser] 
        def get(self,request):
             try:
                  
                    thirty_days_ago = timezone.now() - timedelta(days=30)
                    notifs=Notifications.objects.filter(recipient=request.user ,timestamp__gte=thirty_days_ago).order_by('-timestamp')
                   
                    serializer=notificationAdminSerializer(notifs,many=True)
                        
                    
                    
                    return Response({'payload':serializer.data,'status':200})
             except Exception as e:
                    return Response({'error':str(e),'status':400})
             
        # mark as read
        def patch(self,request):
             try:
                  notifs=Notifications.objects.filter(recipient=request.user ,is_read=False)
                  for noti in notifs:
                       noti.is_read=True
                       noti.save()
                  return Response({'status':200,'message':'Marked notifications as read'})
             except Exception as e:
                  return Response({'error':str(e),'status':400})
             