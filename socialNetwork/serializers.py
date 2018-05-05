from rest_framework import serializers
from django.contrib.auth.models import User
from .models import ProfileModel, PostsModel, GroupModel, FriendshipModel, CommentModel

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ('password', 'email',)

class ProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model = ProfileModel
    fields = ('name', 'mobile', 'birthday', 'gender')
        

class CommentSerializer(serializers.ModelSerializer):
  class Meta:
    model = CommentModel
    fields = '__all__'


class PostsSerializer(serializers.ModelSerializer):
  # comments = CommentSerializer()
  class Meta:
    model = PostsModel
    fields = '__all__'
  
class GroupSerializer(serializers.ModelSerializer):
  class Meta:
    model = GroupModel
    fields = '__all__'
  
class Friendshiperializer(serializers.ModelSerializer):
  class Meta:
    model = FriendshipModel
    fields = '__all__'