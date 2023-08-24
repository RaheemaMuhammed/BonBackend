from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import * 
from django.contrib.auth import authenticate, login
from  rest_framework_simplejwt.authentication import JWTAuthentication
# Create your views here
from rest_framework_simplejwt.tokens import RefreshToken
from .emails import send_otp_via_email
from payment.models import PaymentRequest
# to handle registration


class Register(APIView):
    def post(self,request):
        try:
            data=request.data

            serializer=RegisterSerializer(data=data)

            if serializer.is_valid():

                serializer.save()
                send_otp_via_email(data['email'])
                return Response({'status':200,
                                 'message':'Successfully Registered.Please Check your email',
             
                                 'data':serializer.data})
            return Response({'status':400,
                             'message':'User With this email or mobile number already exists',
                             'error':serializer.errors
                             
                             })

        except Exception as e:
            return Response(
                {
                    'status': 500,
                    'message': 'An error occurred during registration.',
                    'error': str(e)
                })

class VerifyOTP(APIView):
    def post(self,request):
        try:
            data=request.data
            serializer=VerifyEmailSerializer(data=data)

            if serializer.is_valid():
                email=serializer.data['email']
                otp=serializer.data['otp']

                user=CustomUser.objects.filter(email=email)
                if not user.exists():
                    return Response({'status':400,
                                    'message':'something went wrong',
                                    'data':'Invalid email'
                                    })
                if user[0].otp != otp:
                    return Response({'status':400,
                                    'message':'something went wrong',
                                    'data':'Wrong OTP'
                                    })
                user=user.first()
               
                user.is_active = True
                user.is_user= True
                user.otp=""        
                
                user.save()
                return Response({'status':200,
                                 'message':'Email Verification Done',
                                 'data':''})
        except Exception as e:
            return Response(
                {
                    'status': 500,
                    'message': 'An error occurred during Email Verified.',
                    'error': str(e)
                })

class Login(APIView):
    def post(self,request):
        try:
            data=request.data
            email=data['email']
            password=data['password']
           
            user=authenticate(email=email,password=password)
            
            if user is not None:
                obj = CustomUser.objects.get(email=email)
                
                if obj.is_user == True:
                    person = 'user'
                    latest_payment_request=PaymentRequest.objects.filter(user=user).order_by('-created_at').first()
                    
                    if latest_payment_request is not None:
                        if latest_payment_request.status == 'Accepted':
                            requested=True
                        else:
                            requested=False
                    else:
                        requested=False
                    
                
                if obj.is_superuser == True:
                    requested=False
                    person = 'admin'
                if user.is_active == True and user.is_block == False:
                    username=user.username
                    # if not user.is_premium_active():
                    #     user.has_premium=False
                    #     user.save() 
                    premium=user.has_premium
                   
                    login(request,user)
                   
                    refresh=RefreshToken.for_user(user)
                    
                    return Response({'message':'you are successfully logged in',
                                    'status':200,
                                    'refresh':str(refresh),
                                    'access':str(refresh.access_token),
                                    'username':username,
                                    'person':person,
                                    'premium':premium,
                                    'requested': requested

                    })
                elif user.is_block == True:
                    return Response({
                        'status':700,
                        'message':'you are blocked'
                    })
                else:
                    return Response({
                        'status':800,
                        'message':'something happened'
                    })
                
            else:
                return Response({
                    'status':404,
                    'message':'invalid email or password'
                })
        except Exception as e:
            return Response({'error':e})