from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from payment.models import PaymentRequest


@receiver(post_save,sender=PaymentRequest)
def send_payment_request_status_email(sender,instance,**kwargs):
    if instance.status == 'Completed':
       
        subject = 'Payment Request Completed'
        message = f'Your payment request with ID {instance.id} has been completed. Amount: {instance.amount}'
        email_from=settings.EMAIL_HOST_USER
        email=instance.user.email
        send_mail(subject, message,email_from,[email])
    elif instance.status == 'Cancelled':
       

        subject = 'Payment Request Completed'
        message = f'Your payment request with ID {instance.id} has been Cancelled. Amount: {instance.amount}'
        email_from=settings.EMAIL_HOST_USER
        email=instance.user.email
        send_mail(subject, message,email_from,[email])
    else:
        pass