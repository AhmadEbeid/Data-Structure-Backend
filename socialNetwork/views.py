from rest_framework_jwt.settings import api_settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.http import Http404,HttpResponse

from .serializers import UserSerializer, ProfileSerializer, PostsSerializer, GroupSerializer, Friendshiperializer

from .models import ProfileModel, PostsModel, GroupModel, FriendshipModel

# Create your views here.


class SignInView(APIView):
  def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = User.objects.get(username=request.data["email"])
            except User.DoesNotExist:
                return Response({"error": "Email/Password is incorrect"}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                if authenticate(username=user.username,password=request.data["password"]):
                    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
                    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
                    payload = jwt_payload_handler(user)
                    token = jwt_encode_handler(payload)
                    return Response({"token": token}, status=status.HTTP_201_CREATED)
                else:
                    return Response({"error": "Email/Password is incorrect"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignUpView(APIView):
  def post(self, request):
        userSerializer = UserSerializer(data=request.data)
        profileSerializer = ProfileSerializer(data=request.data)
        if userSerializer.is_valid() and profileSerializer.is_valid():
            try:
                User.objects.get(email=request.data["email"])
            except User.DoesNotExist:
                try:
                    user = User.objects.create_user(username=request.data["email"],email=request.data["email"],password=request.data["password"])
                    profile = ProfileModel.objects.create(
                      user = user,
                      name=request.data["name"],
                      mobile=request.data["mobile"],
                      birthday=request.data["birthday"],
                      gender=request.data["gender"]
                    )
                except:
                    Response({"error": "Please try again later"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
                
                jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
                jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
                payload = jwt_payload_handler(user)
                token = jwt_encode_handler(payload)
                
                return Response({"token": token}, status=status.HTTP_201_CREATED)
            else:
                return Response({"error": "The Email Already Exists!"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({"profile":profileSerializer.errors,"user":userSerializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class MyPostsView(APIView):
  # get my posts
  def get(self, request):
    try:
        token = request.META.get('HTTP_AUTHORIZATION', '')
        # token = token.split(" ")[1]
        token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjozLCJ1c2VybmFtZSI6ImEuZWJlaWRAaG90bWFpbC5jb20iLCJleHAiOjE1MjU0NjI1MjUsImVtYWlsIjoiYS5lYmVpZEBob3RtYWlsLmNvbSJ9.YpW0-kIO6wd7DOch1e8FTI7wmqtsFQh_J-L4RgZ8QAA"
        jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
    except :
        return Response({"error": "2-user isn't authorized"}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        try:
            token_info = jwt_decode_handler(token)  # decrypting the token
        except :
            return Response({"error": "token can't be decrypted"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            # getting user from the email sent in
            user = User.objects.get(email=token_info["email"])
            posts = PostsModel.objects.filter(user=user, group=False)
            serializer = PostsSerializer(posts, many=True)
            json = serializer.data
            for post in json:
              print(post)
              user = User.objects.get(pk=int(post['user']))
              post['user'] = {"name":ProfileModel.objects.get(user=user).name, "id": post['user']}
              likes = []
              for id in post['likes']:
                user = User.objects.get(pk=id)
                likes.append({"name":ProfileModel.objects.get(user=user).name, "id": id})
              post['likes'] = likes
            return Response(json, status=status.HTTP_200_OK)
  
  # create new post on wall
  def post(self, request):
    try:
        token = request.META.get('HTTP_AUTHORIZATION', '')
        # token = token.split(" ")[1]
        token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjozLCJ1c2VybmFtZSI6ImEuZWJlaWRAaG90bWFpbC5jb20iLCJleHAiOjE1MjU0NjI1MjUsImVtYWlsIjoiYS5lYmVpZEBob3RtYWlsLmNvbSJ9.YpW0-kIO6wd7DOch1e8FTI7wmqtsFQh_J-L4RgZ8QAA"
        jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
    except :
        return Response({"error": "2-user isn't authorized"}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        try:
            token_info = jwt_decode_handler(token)  # decrypting the token
        except :
            return Response({"error": "token can't be decrypted"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            # getting user from the email sent in
            user = User.objects.get(email=token_info["email"])
            posts = PostsModel.objects.create(user=user, group=False, text=request.data['text'])
            serializer = PostsSerializer(posts)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class postGetView(APIView):
  # get a post with ID
  def get(self, request, pk):
    try:
        token = request.META.get('HTTP_AUTHORIZATION', '')
        # token = token.split(" ")[1]
        token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjozLCJ1c2VybmFtZSI6ImEuZWJlaWRAaG90bWFpbC5jb20iLCJleHAiOjE1MjU0NjI1MjUsImVtYWlsIjoiYS5lYmVpZEBob3RtYWlsLmNvbSJ9.YpW0-kIO6wd7DOch1e8FTI7wmqtsFQh_J-L4RgZ8QAA"
        jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
    except :
        return Response({"error": "2-user isn't authorized"}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        try:
            token_info = jwt_decode_handler(token)  # decrypting the token
        except :
            return Response({"error": "token can't be decrypted"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            # getting user from the email sent in
            user = User.objects.get(email=token_info["email"])
            posts = PostsModel.objects.get(pk=pk)
            serializer = PostsSerializer(posts)
            postS = serializer.data
            user = User.objects.get(pk=int(postS['user']))
            postS['user'] = {"name":ProfileModel.objects.get(user=user).name, "id": postS['user']}
            likes = []
            for id in postS['likes']:
              user = User.objects.get(pk=id)
              likes.append({"name":ProfileModel.objects.get(user=user).name, "id": id})
            postS['likes'] = likes
            return Response(postS, status=status.HTTP_200_OK)
  
  # Like post
  def post(self, request, pk):
    try:
        token = request.META.get('HTTP_AUTHORIZATION', '')
        # token = token.split(" ")[1]
        token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjozLCJ1c2VybmFtZSI6ImEuZWJlaWRAaG90bWFpbC5jb20iLCJleHAiOjE1MjU0NjI1MjUsImVtYWlsIjoiYS5lYmVpZEBob3RtYWlsLmNvbSJ9.YpW0-kIO6wd7DOch1e8FTI7wmqtsFQh_J-L4RgZ8QAA"
        jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
    except :
        return Response({"error": "2-user isn't authorized"}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        try:
            token_info = jwt_decode_handler(token)  # decrypting the token
        except :
            return Response({"error": "token can't be decrypted"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            # getting user from the email sent in
            user = User.objects.get(email=token_info["email"])
            posts = PostsModel.objects.get(pk=pk)
            print(posts.likes.all())
            if request.data["like"] == "true":
              if not user in posts.likes.all():
                posts.likes.add(user)
                posts.save()
            elif request.data["like"] == "false":
              if user in posts.likes.all():
                posts.likes.remove(user)
                posts.save()
            serializer = PostsSerializer(posts)
            postS = serializer.data
            user = User.objects.get(pk=int(postS['user']))
            postS['user'] = {"name":ProfileModel.objects.get(user=user).name, "id": postS['user']}
            likes = []
            for id in postS['likes']:
              user = User.objects.get(pk=id)
              likes.append({"name":ProfileModel.objects.get(user=user).name, "id": id})
            postS['likes'] = likes
            return Response(postS, status=status.HTTP_200_OK)
    
  # delete post
  def delete(self, request, pk):
    try:
        token = request.META.get('HTTP_AUTHORIZATION', '')
        # token = token.split(" ")[1]
        token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjozLCJ1c2VybmFtZSI6ImEuZWJlaWRAaG90bWFpbC5jb20iLCJleHAiOjE1MjU0NjI1MjUsImVtYWlsIjoiYS5lYmVpZEBob3RtYWlsLmNvbSJ9.YpW0-kIO6wd7DOch1e8FTI7wmqtsFQh_J-L4RgZ8QAA"
        jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
    except :
        return Response({"error": "2-user isn't authorized"}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        try:
            token_info = jwt_decode_handler(token)  # decrypting the token
        except :
            return Response({"error": "token can't be decrypted"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            # getting user from the email sent in
            user = User.objects.get(email=token_info["email"])
            try:
              PostsModel.objects.get(user=user, pk=pk).delete()
              return Response(status=status.HTTP_200_OK)
            except:
              return Response(status=status.HTTP_400_BAD_REQUEST)
        

class userProfilePageView(APIView):
  # return profile info, posts
  def get(self, request, pk):
    user = User.objects.get(pk=pk)
    profile = ProfileModel.objects.get(user=user)
    profileSerializer = ProfileSerializer(profile)
    posts = PostsModel.objects.filter(user=user, group=False)
    postSerializer = PostsSerializer(posts, many=True)

    postJson = postSerializer.data
    for post in postJson:
      user = User.objects.get(pk=int(post['user']))
      post['user'] = {"name":ProfileModel.objects.get(user=user).name, "id": post['user']}
      likes = []
      for id in post['likes']:
        user = User.objects.get(pk=id)
        likes.append({"name":ProfileModel.objects.get(user=user).name, "id": id})
      post['likes'] = likes
  
    return Response({"profile":profileSerializer.data,"post":postJson})


# class GroupPostsView(APIView):
#   # get current my posts
#   def get(self, request):


# class AllGroupsView(APIView):
#   # search groups
#   def get(self, request, value):

#   # join group
#   def post(self, request):


# class MyGroupsView(APIView):
#   # get current joined groups
#   def get(self, request):
  
#   # delete group
#   def delete(self, request, pk):
  

# class AllFriendsView(APIView):
#   # get my friend friends
#   def get(self, request, pk):
  

# class MyFriendsView(APIView):
#   # get my friends
#   def get(self, request):
  
#   # unfriend
#   def delete(self, request, pk):


# class PeopleView(APIView):
#   # search for friend
#   def get(self, request, value):

#   # add friend
#   def post(self, request, pk):

