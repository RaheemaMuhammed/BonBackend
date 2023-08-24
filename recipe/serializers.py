from rest_framework import serializers
from . models import *


class CategorySerializer(serializers.ModelSerializer):
    status=serializers.BooleanField(source='is_disabled')
    class Meta:
        model = Categories
        fields = ['name','id','is_disabled','status']
    def validate(self, data):
        if data['name']:
            if any(char.isdigit() for char in data):
                raise serializers.ValidationError("Category name cannot contain numbers.")
            return data
class RecipeSerializer(serializers.ModelSerializer):
    author_id = serializers.CharField(source='author.id')
    author = serializers.CharField(source='author.username')
    author_profile= serializers.ImageField(source='author.profile_pic')
    category_name = serializers.CharField(source='category.name')
    comments=serializers.PrimaryKeyRelatedField(many=True,read_only=True)
    status=serializers.BooleanField(source='is_disabled')
    category = CategorySerializer()

    class Meta:
        model = Recipe
        fields = ('id','author_profile','category', 'category_name', 'picture', 'recipe_name', 'instructions','is_private',
                  'ingredients','created_at','updated_at','author_id','author','revenue','total_reports','comments','total_likes','is_disabled','status')
 

class PostRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Recipe
        fields='__all__'

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'

class SavedRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedRecipes
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user_id.username')
    user_profile = serializers.ImageField(source='user_id.profile_pic')
    children = serializers.SerializerMethodField()
    is_parent = serializers.SerializerMethodField()
    recipe=serializers.CharField(source='recipe_id.recipe_name')
    date=serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('id', 'user', 'recipe_id', 'recipe','comment','date', 'created_at', 'user_profile', 'parent', 'children', 'is_parent')

    def get_date(self,instance):
        return instance.created_at.strftime('%Y-%m-%d')

    def get_children(self, obj):
        children_qs = obj.replies.all()  
        serializer = CommentSerializer(children_qs, many=True)
        return serializer.data

    def get_is_parent(self, obj):
        return obj.parent is None

class PostCommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Comment
        fields='__all__'

class notificationSerializer(serializers.ModelSerializer):
    recipe_name=serializers.CharField(source='post.recipe_name')
    class Meta:
        model=Notifications
        fields=('id','sender','recipient','message','timestamp','is_read','post','recipe_name')

class notificationAdminSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Notifications
        fields=('id','sender','recipient','message','timestamp','is_read')
class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model=Report
        fields='__all__'