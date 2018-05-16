from rest_framework import serializers
from django.contrib.auth.models import User
from .models import ProfileModel, PostsModel, GroupModel, FriendshipModel, CommentModel
from BackEnd.fields import Base64FileField

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ('password', 'email',)

class ProfileSerializer(serializers.ModelSerializer):
  image = Base64FileField(max_length=None,use_url=True,required=False)
  class Meta:
    model = ProfileModel
    fields = ('name', 'mobile', 'birthday', 'gender', 'image')
        
class ProfileSerializer2(serializers.ModelSerializer):
  image = Base64FileField(max_length=None,use_url=True,required=False)
  class Meta:
    model = ProfileModel
    fields = ('name', 'mobile', 'birthday', 'gender', 'image', 'pk')
        

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
  
class FriendshipSerializer(serializers.ModelSerializer):
  class Meta:
    model = FriendshipModel
    fields = '__all__'