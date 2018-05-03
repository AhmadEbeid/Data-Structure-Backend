from datetime import timedelta
from django.contrib.auth.models import User
from django.db import models
#from jsonfield import JSONField
from django.contrib.postgres.fields import JSONField
import json

# Create your models here.

gender=[('Male','Male'), ('Female','Female')]

class ProfileModel(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, related_name='profile')
  name = models.CharField(max_length=255)
  mobile = models.CharField(max_length=15, unique=True)
  birthday = models.DateField()
  gender = models.CharField(max_length=15, choices=gender)
  created_date = models.DateField(auto_now=True)

  def __str__(self):
      return self.user.__str__() + ' Name: ' + self.name.__str__()

class FriendshipModel(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, related_name='friends')
  friendsList = models.ManyToManyField(User)

  def __str__(self):
      return self.user.__str__()

class PostsModel(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, related_name='posts')
  group = models.BooleanField(default=False)
  text = models.TextField(max_length=5000)
  likes =  models.ManyToManyField(User, blank=True)
  created_date = models.DateField(auto_now=True)

  def __str__(self):
      return self.user.__str__() + ' Text: ' + self.text.__str__()

class GroupModel(models.Model):
  name = models.CharField(max_length=100)
  description = models.TextField(max_length=5000)
  users = models.ManyToManyField(User, blank=True)
  admin = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, related_name='groupAdmin')
  posts =  models.ManyToManyField(PostsModel, blank=True)

  def __str__(self):
      return self.name.__str__() + ' Admin: ' + self.admin.__str__()
