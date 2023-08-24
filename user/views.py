from django.utils import timezone
from datetime import timedelta
from hitcount.models import HitCount
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.shortcuts import render
from recipe.serializers import *
from rest_framework.views import APIView
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.response import Response
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from recipe.models import *
from adminpanel.models import Categories
from decimal import Decimal
from adminpanel.serializers import UserSerializer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from account.serializers import RegisterSerializer
from django.db.models import Count
# Create your views here.

class RecipeList(APIView):
     # verifies authenticated using jwt
    authentication_classes = [JWTAuthentication]
    # verifies user is adminuser
    permission_classes = [IsAuthenticated] 


    # Adding Recipes 
    def post(self,request):
        try:
            data=request.data
            print(data)
            recipe_name = request.data['recipe_name']
            data=data.copy()
            author=CustomUser.objects.get(username=data['author'])
            data['author']=author.id
            serializer = PostRecipeSerializer(data=data)
            if not serializer.is_valid():
                return Response({'status':300,'error':serializer.errors,'message':'something went wrong'})
            serializer.save()
            return Response({'status':200,'message':f'Recipe {recipe_name} is added successfully'})
        except Exception as e:
            return Response({'error':str(e)})

    # Listing all the recipes
    def get(self,request):
            try:
                recipes=Recipe.objects.filter(is_private=False).order_by('-id')
                serializer=RecipeSerializer(recipes,many=True)
                return Response({'payload':serializer.data,'message':'success'})
            except Exception as e:
                return Response({'error':str(e)})
            
    # editing recipe

    def patch(self,request):
         data=request.data
         print(data)
         try:
                recipe=Recipe.objects.get(id=data['id'])
                print(recipe)
                serializer=PostRecipeSerializer(instance=recipe,data=data,partial=True)
                if not serializer.is_valid():
                    return Response({'status':300,'error':serializer.errors,'message':'somthing for serializer'})   
                serializer.save()
                return Response({'status':200,'message': f'{recipe} updated successfully'})

         except Exception as e:
              return Response({'error':str(e)})
         

    # deleting a recipe
    def delete(self,request):
            try:
                 id=request.GET.get('id')
                 print(id)
                 recipe=Recipe.objects.get(id=id)
                 recipe.delete()
                 return Response({'status':200,'message':f'Recipe {recipe} deleted successfully'})
            except Exception as e:
                 return Response({'error':str(e)})

# Get single recipe

class SingleRecipe(APIView):
        authentication_classes = [JWTAuthentication]
        permission_classes = [IsAuthenticated]
        def get(self,request):
            
            try:
                recipe_name = request.GET.get('recipe_name')
                recipe = Recipe.objects.get(recipe_name=recipe_name)
               
                serializer = RecipeSerializer(recipe)
                return Response({'status':200,'payload':serializer.data})
            except Exception as e:
                return Response({'error':str(e)})

class CategoryListing(APIView):
        authentication_classes = [JWTAuthentication]
        permission_classes = [IsAuthenticated]
        def get(self,request):
            try:
                categories=Categories.objects.filter(is_disabled=False).order_by('-id')
                filtered_categories=Categories.objects.filter(is_disabled=False).annotate(recipe_count=Count('recipe')).filter(recipe_count__gt=0).order_by('-id')
                serializer=CategorySerializer(categories,many=True)
                serializer_filtered=CategorySerializer(filtered_categories,many=True)
                return Response({'payload':serializer.data,'message':'success','filtered_categories':serializer_filtered.data})
            except Exception as e:
                return Response({'error':str(e)})
            
# For Liking and removing like
class LikeRecipe(APIView):
      authentication_classes = [JWTAuthentication]
      permission_classes = [IsAuthenticated]

      def get(self,request):
           try:
                user=request.user.id
                liked_recipes=Recipe.objects.filter(like__user_id=user)
                serializer=RecipeSerializer(liked_recipes,many=True)
                return Response({'payload':serializer.data,'status':200})
           except Exception as e:
                return Response({'error':str(e)})

      def patch(self,request):
            try:
                data=request.data
                recipe_id=data['recipe_id']
                recipe = Recipe.objects.get(pk=recipe_id)
                user=request.user
    

                try:
                    like= Like.objects.get(user_id=user,recipe_id=recipe)
                    like.delete()
                    recipe.total_likes-=1
                    author_id=recipe.author.id
                    author=CustomUser.objects.get(pk=author_id)
                    if author.wallet > 0.05 and recipe.is_private==True:
                        author.wallet=Decimal(author.wallet)-Decimal('0.05')
                        author.save()
                        print(author.wallet,author.uername)
                except Like.DoesNotExist:
                        Like.objects.create(user_id=user,recipe_id=recipe)
                        recipe.total_likes+=1
                        author_id=recipe.author.id

                        if recipe.is_private == True:
                            author=CustomUser.objects.get(pk=author_id)
                            author.wallet=Decimal(author.wallet)+Decimal('0.05')
                            author.save()
                            print(author.wallet,author.uername)
                        notification_message=f"{user.username} liked your recipe :{recipe.recipe_name}"
                        Notifications.objects.create(sender=user,recipient=recipe.author,post=recipe,message=notification_message,is_read=False)
                        print('likedd')

                        channel_layer=get_channel_layer()
                        author_channel_name=f"user_{recipe.author.id}"
                        print(author_channel_name)
                        
                    
                        async_to_sync(channel_layer.group_send)(
                             author_channel_name,
                             {
                                  "type":"send_notification",
                                  "notification":{
                                       "message":notification_message,
                                       "is_read":False,
                                  },
                             },
                        )
                       


                recipe.save()
                serializer=RecipeSerializer(recipe,partial=True)
                return Response(serializer.data)

                 
            except Exception as e:
                 return Response({'error':str(e)})
            
# For recipe saving
class SavedRecipe(APIView):
      authentication_classes = [JWTAuthentication]
      permission_classes = [IsAuthenticated]

      def get(self,request):
           try:
                user=request.user.id
                saved_recipes=SavedRecipes.objects.filter(user_id=user)
                recipe_ids=saved_recipes.values_list('recipe_id',flat=True)
                recipes=Recipe.objects.filter(pk__in=recipe_ids)
                serializer=RecipeSerializer(recipes,many=True)
                return Response({'payload':serializer.data,'status':200})
           except Exception as e:
                return Response({'error':str(e)})
           

      def patch(self,request):
            try:
                data=request.data
                recipe_id=data['recipe_id']
                recipe=Recipe.objects.get( pk=recipe_id)

                if recipe_id is not None:
                        user=request.user
                        try:
                            saved_recipe=SavedRecipes.objects.get(user_id=user,recipe_id=recipe_id)
                            saved_recipe.delete()
                            author_id=recipe.author.id
                            author=CustomUser.objects.get(pk=author_id)
                            if author.wallet > 0.05 and recipe.is_private == True:
                                author.wallet=Decimal(author.wallet)-Decimal('0.05')
                                author.save()
                            return Response({'status':200,'message':'Recipe Removed Successfully'})
                        except SavedRecipes.DoesNotExist:
                            
                            SavedRecipes.objects.create(user_id=user,recipe_id=recipe)
                            author_id=recipe.author.id
                            if recipe.is_private == True:
                                    author=CustomUser.objects.get(pk=author_id)
                                    author.wallet=Decimal(author.wallet)+Decimal('0.05')
                                    
                                    author.save()
                            return Response({'status':200,'message':'Recipe Added to Saved List Successfully'})
            except Exception as e:
                return Response({'error':str(e)})

# List recipes of current user
class UserRecipe(APIView):
        authentication_classes = [JWTAuthentication]
        permission_classes = [IsAuthenticated]
   
        # list current user's recipes
        def get(self,request):
             try:
                user=request.user
                recipes=Recipe.objects.filter(author=user)
                recipe_data=[]
                for recipe in recipes:
                     try:
                         hit_count = recipe.views.get()
                         view_count = hit_count.hits
                     except HitCount.DoesNotExist:
                         view_count = 0
                     serializer=RecipeSerializer(recipe)
                     recipe_data.append({'recipe':serializer.data,'view_count':view_count})
                return Response({'payload':recipe_data,'status':200})
             except Exception as e:
                  return Response({'error':str(e)})
                  
        # editing recipe

        def patch(self,request):
            data=request.data
            try:
                    recipe=Recipe.objects.get(id=data['recipe_id'])
                    print(recipe)
                    serializer=PostRecipeSerializer(instance=recipe,data=data,partial=True)
                    print(data)
                    if not serializer.is_valid():
                        return Response({'status':300,'error':serializer.errors,'message':'somthing for serializer'})   
                    serializer.save()
                    return Response({'status':200,'message': f'{recipe} updated successfully'})

            except Exception as e:
                return Response({'error':str(e)})
            

        # deleting a recipe
        def delete(self,request):
                try:
                    id=request.GET.get('id')
                    recipe=Recipe.objects.get(id=id)
                    recipe.delete()
                    return Response({'status':200,'message':f'Recipe {recipe} deleted successfully'})
                except Exception as e:
                    return Response({'error':str(e)})

     
# profile page for users and editing
class UserProfile(APIView):
        authentication_classes = [JWTAuthentication]
        permission_classes = [IsAuthenticated]
        # get details
        def get(self,request):
             try:
                  id=request.user.id
                  user=CustomUser.objects.get(pk=id)
                  serializer=UserSerializer(user)
                  return Response({'payload':serializer.data,'message':'OK','status':200})
             except Exception as e:
                  return Response({'error':str(e)})

        
        # edit profile
        def patch(self,request):
            data=request.data
            if not data:
                return Response({'error': 'Request body is empty', 'status': 404})
            try:
                profile=CustomUser.objects.get(id=request.user.id)
               
                serializer = RegisterSerializer(profile, data=data, partial=True)
                
                
                if serializer.is_valid():
                    serializer.save() 
                    return Response({'message': 'Profile updated successfully', 'status': 200})
                else:
                    return Response({'error': serializer.errors, 'status': 400})
            except Exception as e:
                return Response({'error': str(e), 'status': 500})
                    
                
           
# comment system
class Comments(APIView):
        authentication_classes = [JWTAuthentication]
        permission_classes = [IsAuthenticated]

        def post(self,request):
             try:
                  
                    data=request.data
                   
                    recipe=data['recipe_id']
                    user_id=request.user.id
                    data['user_id']=user_id
                    user=CustomUser.objects.get(pk=user_id)
                    this_recipe=Recipe.objects.get(pk=recipe)
                    serializer=PostCommentsSerializer(data=data)
                    if serializer.is_valid():
                        serializer.save()
                        notification_message=f"{user.username} commented {data['comment']}"
                        
                        Notifications.objects.create(sender=user,recipient=this_recipe.author,post=this_recipe,message=notification_message,is_read=False)
                        
                        channel_layer=get_channel_layer()
                        author_channel_name=f"user_{this_recipe.author.id}"
                        async_to_sync(channel_layer.group_send)(
                             author_channel_name,
                             {
                                  "type":"send_notification",
                                  "notification":{
                                       "message":notification_message,
                                       "is_read":False,
                                  },
                             },
                        )
                        return Response({'status':200,'message':'Comment Posted successfully'})
                    return Response({'status':400,'message':'Invalid Data'})
             except Exception as e:
                  return Response({'error':str(e)})
                    
        
        def delete(self,request):
            try:
                 id=request.GET.get('id')
                 comment=Comment.objects.get(pk=id)
                 comment.delete()
                 return Response({'status':200,'message':' Deleted successfully'})
            except Exception as e:
                 return Response({'error':str(e)})
     
# get latest notification
class Notification(APIView):
        authentication_classes = [JWTAuthentication]
        permission_classes = [IsAuthenticated] 
        def get(self,request):
             try:
                  
                    thirty_days_ago = timezone.now() - timedelta(days=5)
                    notifs=Notifications.objects.filter(recipient=request.user ,timestamp__gte=thirty_days_ago).order_by('-timestamp')
                    
                         
                    serializer=notificationSerializer(notifs,many=True)
                    
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
             
# for reporting a recipe
class Reports(APIView):
     authentication_classes = [JWTAuthentication]
     permission_classes = [IsAuthenticated] 
     def post(self,request):
        try:
            data=request.data
            user=request.user.id
            recipe_id=data['reported_item']
            data['user']=user
            recipe=Recipe.objects.get(pk=recipe_id)
            serializer=ReportSerializer(data=data)
            if serializer.is_valid():
                 recipe.total_reports+=1
                 recipe.save()
                 serializer.save()
                 return Response({'status':200,'message':f'Recipe {recipe.recipe_name} is reported successfully'})
            return Response({'status':400,'message':serializer.errors})
        except Exception as e:
            return Response({'error':str(e)})
        
class TrackRecipeView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        data=request.data
        recipe_id = data['recipe_id']
        
        if not recipe_id:
            return Response({'error': 'Recipe ID is required.', 'status':400})
        
        try:
            recipe = Recipe.objects.get(pk=recipe_id)
       
        except Recipe.DoesNotExist:
            return Response({'error': 'Recipe not found.', 'status':400})
        content_type =ContentType.objects.get_for_model(Recipe)
        object_pk=str(recipe.pk)
        hit_count, created = HitCount.objects.get_or_create(
          content_type=content_type,
          object_pk=object_pk
        )
        hit_count.increase()
        
        return Response({'message': 'Recipe view tracked.','status':200})
    

# search suggestions
class Suggestions(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request):
         try:
              
                term=request.GET.get('term')
                matching_recipes=self.get_suggestions(Recipe,'recipe_name',term)
                matching_cats=self.get_suggestions(Categories,'name',term)
                
                
                suggestion=matching_recipes+matching_cats
                
                
                return Response({'payload':suggestion,'status':200})
         except Exception as e:
              return Response({'error':str(e),'status':400})
    
    def get_suggestions(self,model,field,term):
                matching_objects=model.objects.filter(**{f'{field}__icontains':term})
                suggestions = [getattr(obj,field) for obj in matching_objects]
                return suggestions
         
class Search(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
         try:
              
            query=request.GET.get('query')
            matching_recipes=Recipe.objects.filter(Q(recipe_name__icontains=query) | Q(category__name__icontains=query) | Q(author__username__icontains=query) | Q(ingredients__icontains=query))
            # print(matching_recipes.recipe_name)
            serializer=RecipeSerializer(matching_recipes,many=True)
            return Response({'payload':serializer.data,'status':200})
         except Exception as e:
            return Response({'error':str(e),'status':400})
         
         
class Filter(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
         try:
              
            query=request.GET.get('query')
            matching_recipes=Recipe.objects.filter(category__name=query)
            # print(matching_recipes.recipe_name)
            serializer=RecipeSerializer(matching_recipes,many=True)
            return Response({'payload':serializer.data,'status':200})
         except Exception as e:
            return Response({'error':str(e),'status':400})
         
