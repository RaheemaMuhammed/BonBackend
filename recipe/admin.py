from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Recipe)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(SavedRecipes)
admin.site.register(Notifications)
admin.site.register(Report)