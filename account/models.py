from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager,PermissionsMixin
import uuid
from django.utils import timezone
import json
# Create your models here.

class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    def _create_user(self, email,phone, password=None, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email,phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email,phone,password, **extra_fields)

    def create_superuser(self, email,phone, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True )

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, phone,password, **extra_fields)
        


class CustomUser(AbstractUser,PermissionsMixin):
    email=models.EmailField(max_length=100, unique=True)
    phone=models.IntegerField(unique=True,null=True)
    username=models.CharField(max_length=250,null=True)
    has_premium=models.BooleanField(default=False)
    is_block=models.BooleanField(default=False)
    premium_expiry=models.DateTimeField(null=True)
    wallet=models.DecimalField(default=0,decimal_places=2,max_digits=5)
    profile_pic=models.ImageField(null=True,upload_to='userprofile/')
    is_active=models.BooleanField(default=False)
    is_user=models.BooleanField(default=False)
    otp=models.CharField(max_length=6,null=True,blank=True)
    transaction_history = models.TextField(default='[]')
    total_reports=models.IntegerField(default=0)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone','username']

    objects = CustomUserManager()


    def is_premium_active(self):
        if self.premium_expiry is not None and self.premium_expiry >= timezone.now():
            return True
        return False
    def has_private_recipe(self):
        return self.recipe_set.filter(is_private=True).exists()
    def __str__(self):  
        return f'{self.username}'


    def get_transaction_history(self):
        return json.loads(self.transaction_history)

    def add_transaction(self, transaction_details):
        history = self.get_transaction_history()
        history.append(transaction_details)
        self.transaction_history = json.dumps(history)
        self.save()




