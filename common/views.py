from django.shortcuts import render
from rest_framework.views import APIView
from recipe.serializers import *
from recipe.models import *
from rest_framework.response import Response
from decimal import Decimal
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination

class MyPageNumberPagination(PageNumberPagination):
     page_size = 3  # Number of items per page

class RecipeList(generics.ListAPIView):
    # Listing all the recipes
   
            queryset=Recipe.objects.filter(is_disabled=False).order_by('-id')
            serializer_class=RecipeSerializer
            pagination_class=MyPageNumberPagination

            
  # Get single recipe

class SingleRecipe(APIView):
 
        def get(self,request):
            try:
                recipe_name = request.GET.get('recipe_name')
                
                recipe = Recipe.objects.get(recipe_name=recipe_name)
                
                counts=recipe.views.all()
                serializer = RecipeSerializer(recipe)
                return Response({'status':200,'payload':serializer.data})
            except Exception as e:
                return Response({'error':str(e)})
            
class AuthorProfile(APIView):
     def get(self,request):
            pass
# Trending recipes
class Trending(APIView):
     def get(self,request):
            try:
                recipes=Recipe.objects.filter(is_disabled=False).order_by('-total_likes')[:8]
                serializer=RecipeSerializer(recipes,many=True)
                return Response({'payload':serializer.data,'message':'success'})
            except Exception as e:
                return Response({'error':str(e)})
            
# latest recipes
class Latest(APIView):
     def get(self,request):
            try:
                recipes=Recipe.objects.filter(is_disabled=False).order_by('-created_at')[:8]
                serializer=RecipeSerializer(recipes,many=True)
                return Response({'payload':serializer.data,'message':'success'})
            except Exception as e:
                return Response({'error':str(e)})
            
class CommentListing(APIView):
  
          def get(self,request):
             try:
                recipe_id = request.GET.get('recipe_id')
                
                recipe=Comment.objects.filter(recipe_id=recipe_id,parent=None)
                
                serializer=CommentSerializer(recipe,many=True)
                return Response({'status':200,'payload':serializer.data})

             except Exception as e:
                  return Response({'error':str(e)})
          
          