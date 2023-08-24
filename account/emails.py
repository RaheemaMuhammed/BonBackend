from django.core.mail import send_mail
import random
from django.conf import settings
from .models import CustomUser

def send_otp_via_email(email):
    subject='Account Verification Email'
    otp= random.randint(100000,999999)
    message=f'Your OTP is {otp}'
    email_from=settings.EMAIL_HOST_USER
    send_mail(subject, message,email_from,[email])
    
    # saving this otp to the corresponding user in the database
    user_obj = CustomUser.objects.get(email=email)
    user_obj.otp=otp
    user_obj.save()


