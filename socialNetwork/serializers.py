from rest_framework import serializers
from django.contrib.auth.models import User
from .models import ProfileModel, PostsModel, GroupModel, FriendshipModel

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ('password', 'email',)

class ProfileSerializer(serializers.ModelSerializer):
  class Meta:
        model = ProfileModel
        fields = ('name', 'mobile', 'birthday', 'gender')
        

class PostsSerializer(serializers.ModelSerializer):
  class Meta:
    model = PostsModel
    fields = '__all__'
  
class GroupSerializer(serializers.ModelSerializer):
  user = UserSerializer()
  admin = UserSerializer()
  class Meta:
    model = GroupModel
    fields = '__all__'
  
class Friendshiperializer(serializers.ModelSerializer):
  user = UserSerializer()
  friendsList = UserSerializer()
  class Meta:
    model = FriendshipModel
    fields = '__all__'