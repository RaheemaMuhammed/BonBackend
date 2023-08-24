from django.urls import path
from .views import *


urlpatterns=[
    path('recipes/',RecipeList.as_view()),
    path('single_recipe/',SingleRecipe.as_view()),
    path('categories/',CategoryListing.as_view()),
    path('like/',LikeRecipe.as_view()),
    path('saved_recipe/',SavedRecipe.as_view()),
    path('user_recipe/',UserRecipe.as_view()),
    path('user_profile/',UserProfile.as_view()),
    path('comments/',Comments.as_view()),
    path('notification/',Notification.as_view()),
    path('report/',Reports.as_view()),
    path('track_view/',TrackRecipeView.as_view()),
    path('suggestions/',Suggestions.as_view()),
    path('search/',Search.as_view()),
    path('filter/',Filter.as_view()),
   
]