from django.contrib import admin
from .models import ProfileModel, FriendshipModel, PostsModel
# Register your models here.
admin.site.register(ProfileModel)
admin.site.register(FriendshipModel)
admin.site.register(PostsModel)

