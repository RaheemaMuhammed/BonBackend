
# from rest_framework import serializers
# from account.models import *

# class ProfileSerializer(serializers.ModelSerializer):
#     recipes=serializers.PrimaryKeyRelatedField(many=True,read_only=True)
#     comments=serializers.PrimaryKeyRelatedField(many=True,read_only=True)

#     class Meta:
#         model = CustomUser
#         fields = ['email', 'phone', 'username', 'premium_expiry', 'id', 'profile_pic','wallet','has_premium','recipes','comments','transaction_history']
