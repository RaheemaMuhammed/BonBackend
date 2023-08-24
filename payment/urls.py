from django.urls import path
from .views import *


urlpatterns = [
    path('payment_start/',start_payment, name="payment"),
    path('payment_success/',handle_payment_success, name="payment_success"),
    path('payment_request/',PaymentRequest.as_view()),

  
]