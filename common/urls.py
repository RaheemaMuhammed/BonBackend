from django.urls import path
from .views import *


urlpatterns=[
    path('recipes/',RecipeList.as_view()),
    path('trending/',Trending.as_view()),
    path('latest/',Latest.as_view()),
    path('single_recipe/',SingleRecipe.as_view()),
    path('author_profile/',AuthorProfile.as_view()),
    path('comments/',CommentListing.as_view())

]