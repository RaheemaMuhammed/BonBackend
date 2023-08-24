from rest_framework import serializers
from .models import *


# for signing up

class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
            model = CustomUser
            fields=['username','email','phone','password','profile_pic']

    def validate(self, data):
        if 'username' in data:
            for i in data['username']:
                if i.isdigit():
                    raise serializers.ValidationError({'error':'name cannot contain numbers'})
        print(data)
               
        if 'phone' in data :
            num=str(data['phone'])
            if len(num)>10 or len(num)<10:
                raise serializers.ValidationError({'error':'invalid phone number'})
        return data
    

    def create(self,validated_data):
        user=CustomUser.objects.create(email=validated_data['email'])
        user.username=validated_data['username']
        user.phone=validated_data['phone']
        user.set_password(validated_data['password'])
        user.save()
        return user 
    
    def update(self, instance, validated_data):
        if 'username' in validated_data:
               instance.username = validated_data.get('username', instance.username)
        if 'email' in validated_data:
               instance.email = validated_data.get('email', instance.email)
        if 'phone' in validated_data:
               instance.phone = validated_data.get('phone', instance.phone)
        if 'profile_pic' in validated_data:
               instance.profile_pic = validated_data.get('profile_pic', instance.profile_pic)
        instance.save()

        return instance
    

class VerifyEmailSerializer(serializers.Serializer):
    email=serializers.EmailField()
    otp=serializers.CharField()

