from django.urls import path
from .views import *


urlpatterns = [
    path('users/',UserList.as_view()),
    path('users/<int:user_id>/',UserList.as_view()),
    path('categories/',CategoryList.as_view()),
    path('payment_requests/',ManageRequest.as_view()),
    path('recipes/',Recipes.as_view()),
    path('analytics/',Analytics.as_view()),
    path('user/notification/',Notification.as_view()),
  
]