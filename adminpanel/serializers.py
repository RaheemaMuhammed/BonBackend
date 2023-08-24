from rest_framework import serializers
from .models import *
from account.models import *
import json
from payment.models import PaymentRequest
from recipe.models import Recipe,Comment
from recipe.serializers import RecipeSerializer,CommentSerializer

class TransactionHistoryField(serializers.Field):
    def to_representation(self, value):
        return json.loads(value)

    def to_internal_value(self, data):
        return json.dumps(data)

class UserSerializer(serializers.ModelSerializer):
    transaction_history = TransactionHistoryField()

    status=serializers.BooleanField(source='is_block')
    class Meta:
        model = CustomUser
        fields = ['email', 'phone', 'username', 'has_premium', 'is_block','id', 'is_active','status', 'is_user','profile_pic','wallet','transaction_history']

class UserDetailSerializer(serializers.ModelSerializer):
    status=serializers.BooleanField(source='is_block')
    transaction_history = TransactionHistoryField()
    recipes = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    class Meta:
        model = CustomUser
        fields = ['email', 'phone', 'username', 'has_premium', 'is_block','wallet' ,'premium_expiry', 'id', 'profile_pic', 'is_active','status', 'is_user','transaction_history','recipes','comments']
    
    def get_recipes(self, obj):
        user_recipes = Recipe.objects.filter(author=obj)
        serializer = RecipeSerializer(user_recipes, many=True)
        return serializer.data

    def get_comments(self, obj):
        user_comments = Comment.objects.filter(user_id=obj)
        serializer = CommentSerializer(user_comments, many=True)
        return serializer.data
        

class PaymentSerializer(serializers.ModelSerializer):
    username=serializers.CharField(source='user.username')
    class Meta:
        model = PaymentRequest
        fields = ('user','id','upi_id','amount','created_at','status','username')

# for graph
class UserAnalyticSerializer(serializers.Serializer):
    date = serializers.DateField()
    regular_users = serializers.IntegerField()
    premium_users = serializers.IntegerField()