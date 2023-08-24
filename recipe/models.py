from django.db import models
from account.models import CustomUser
from adminpanel.models import Categories
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.contrib.contenttypes.fields import GenericRelation
from hitcount.models import HitCountMixin,HitCount
# Create your models here.


class Recipe(models.Model,HitCountMixin):
    author=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='recipes')
    recipe_name=models.CharField(max_length=100)
    category=models.ForeignKey(Categories,on_delete=models.CASCADE)
    picture=models.ImageField(upload_to='media',default='recipe')
    instructions=models.TextField()
    ingredients=models.TextField()
    created_at=models.DateTimeField(auto_now=False,auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True,auto_now_add=False)
    is_private=models.BooleanField(default=False)
    views=GenericRelation(HitCount,object_id_field="object_pk")
    revenue=models.DecimalField(default=0,decimal_places=2,max_digits=5)
    total_reports=models.IntegerField(default=0)
    total_likes=models.PositiveIntegerField(default=0)
    is_disabled=models.BooleanField(default=False)
    def __str__(self) -> str:
        return self.recipe_name
    

class SavedRecipes(models.Model):
    user_id=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    recipe_id=models.ForeignKey(Recipe,on_delete=models.CASCADE)

class Like(models.Model):
    user_id=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    recipe_id=models.ForeignKey(Recipe,on_delete=models.CASCADE)

class Comment(models.Model):
    comment=models.TextField()
    user_id=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='comments')
    recipe_id=models.ForeignKey(Recipe,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now=False,auto_now_add=True)
    parent=models.ForeignKey('self', null=True , blank=True , on_delete=models.CASCADE , related_name='replies')

   

    def __str__(self):
        return str(self.user_id) + ' comment ' + str(self.comment)

    
class Notifications(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_notifications')
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_notifications')
    post=models.ForeignKey(Recipe,on_delete=models.CASCADE,default=None,null=True)
    message = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.sender} -> {self.recipient}: {self.message}' 

class Report(models.Model):
    REPORT_TYPES = (
        ('inappropriate', 'Inappropriate Content'),
        ('spam', 'Spam'),
        ('copied', 'Content Copied'),
        ('other', 'Other'),
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    reported_item = models.ForeignKey(Recipe, on_delete=models.CASCADE) 
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    reason = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report on {self.reported_item} by {self.user}"