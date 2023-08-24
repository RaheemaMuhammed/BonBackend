from celery import shared_task
from datetime import timedelta
from django.utils import timezone
from account.models import CustomUser
from recipe.models import Notifications


@shared_task
def delete_old_notifications():
    threshold_date = timezone.now() - timedelta(days=2)
    Notifications.objects.filter(timestamp__lt=threshold_date).delete()
    return "Old notifications deleted"

@shared_task
def premium_expiry_users():
    current_datetime = timezone.now()
    expired_users = CustomUser.objects.filter(premium_expiry__lt=current_datetime)
    count = CustomUser.objects.filter(premium_expiry__lt=current_datetime).count()
    for user in expired_users:
            user.has_premium = False
            user.save()

    return f"{count} subscriptions expired"

