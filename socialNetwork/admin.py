from django.contrib import admin
from .models import ProfileModel, FriendshipModel, PostsModel, CommentModel
# Register your models here.
admin.site.register(ProfileModel)
admin.site.register(FriendshipModel)
admin.site.register(PostsModel)
admin.site.register(CommentModel)


