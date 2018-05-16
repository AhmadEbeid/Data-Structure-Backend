from rest_framework_jwt.settings import api_settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.http import Http404,HttpResponse
from django.db.models import Q
from django.conf import settings

from .serializers import UserSerializer, ProfileSerializer, ProfileSerializer2, PostsSerializer, GroupSerializer, FriendshipSerializer, CommentSerializer

from .models import ProfileModel, PostsModel, GroupModel, FriendshipModel, CommentModel

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
                    # ProfileModel.objects.create(
                    #   user = user,
                    #   name=request.data["name"],
                    #   mobile=request.data["mobile"],
                    #   birthday=request.data["birthday"],
                    #   gender=request.data["gender"]
                    # )
                    profileSerializer.save(user=user)
                    FriendshipModel.objects.create(user=user)
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
        token = token.split(" ")[1]
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
            print(posts)
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

              comments = []
              for id in post['comments']:
                comment = CommentModel.objects.get(pk=id)
                user = comment.user
                text = comment.text
                comments.append({"name":ProfileModel.objects.get(user=user).name, "id": id, "text":text})
              post['comments'] = comments
            return Response(json, status=status.HTTP_200_OK)
  
  # create new post on wall
  def post(self, request):
    try:
        token = request.META.get('HTTP_AUTHORIZATION', '')
        token = token.split(" ")[1]
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


class wallPosts(APIView):
    def get(self, request):
        try:
            token = request.META.get('HTTP_AUTHORIZATION', '')
            token = token.split(" ")[1]
            jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
        except :
            return Response({"error": "2-user isn't authorized"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            try:
                token_info = jwt_decode_handler(token)  # decrypting the token
                pass
            except :
                return Response({"error": "token can't be decrypted"}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                MainUserID = User.objects.get(email=token_info["email"]).id
                
                que = Q()
                friends = FriendshipModel.objects.get(user=MainUserID)
                dataSerializer = FriendshipSerializer(friends).data
                friendsList = dataSerializer['friendsList']
                for des in friendsList:
                    que = que | Q(user_id=des)
                que = que | Q(user_id=MainUserID)
                posts = PostsModel.objects.filter(group=False).filter(que)
                postSerializer = PostsSerializer(posts, many=True)
                postJson = postSerializer.data
                postJson.reverse()
                for post in postJson:
                    user = User.objects.get(pk=int(post['user']))
                    prof = ProfileModel.objects.get(user=user)
                    post['user'] = {"image":settings.BASE_URL+prof.image.url, "name":prof.name, "id": post['user']}
                    likes = []
                    boolValue = False
                    for id in post['likes']:
                        print(id)
                        print(MainUserID)
                        if MainUserID == id:
                            boolValue = True
                        user = User.objects.get(pk=id)
                        prof = ProfileModel.objects.get(user=user)
                        likes.append({"image":settings.BASE_URL+prof.image.url,"name":prof.name, "id": id})
                    post['likes'] = likes
                    if boolValue:
                        post['liked'] = True
                    else:
                        post['liked'] = False
                    comments = []
                    commentsReverse = post['comments']
                    # reversed(commentsReverse)
                    commentsReverse.reverse()
                    for id in commentsReverse:
                        comment = CommentModel.objects.get(pk=id)
                        user = comment.user
                        text = comment.text
                        prof = ProfileModel.objects.get(user=user)
                        comments.append({"image":settings.BASE_URL+prof.image.url,"name":prof.name, "id": user.id, "text":text})
                    post['comments'] = comments
                return Response(postJson, status=status.HTTP_200_OK)
    

class postGetView(APIView):
  # get wall post with ID
  def get(self, request, pk):
    try:
        token = request.META.get('HTTP_AUTHORIZATION', '')
        token = token.split(" ")[1]
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
            
            comments = []
            for id in postS['comments']:
              comment = CommentModel.objects.get(pk=id)
              user = comment.user
              text = comment.text
              comments.append({"name":ProfileModel.objects.get(user=user).name, "id": id, "text":text})
            postS['comments'] = comments
            return Response(postS, status=status.HTTP_200_OK)
  
  # Like post
  def post(self, request, pk):
    try:
        token = request.META.get('HTTP_AUTHORIZATION', '')
        token = token.split(" ")[1]
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
            comments = []
            for id in postS['comments']:
              comment = CommentModel.objects.get(pk=id)
              user = comment.user
              text = comment.text
              comments.append({"name":ProfileModel.objects.get(user=user).name, "id": id, "text":text})
            postS['comments'] = comments
            return Response(postS, status=status.HTTP_200_OK)
    
  # delete post
  def delete(self, request, pk):
    try:
        token = request.META.get('HTTP_AUTHORIZATION', '')
        token = token.split(" ")[1]
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
        

class postComment(APIView):
    # comment post
  def post(self, request, pk):
    try:
        token = request.META.get('HTTP_AUTHORIZATION', '')
        token = token.split(" ")[1]
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
            comment = CommentModel.objects.create(user=user, text=request.data['commentText'])
            posts.comments.add(comment)
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
            comments = []
            for id in postS['comments']:
              comment = CommentModel.objects.get(pk=id)
              user = comment.user
              text = comment.text
              comments.append({"name":ProfileModel.objects.get(user=user).name, "id": id, "text":text})
            postS['comments'] = comments
            return Response(postS, status=status.HTTP_200_OK)
    

class userProfilePageView(APIView):
  # return profile info, posts
  def get(self, request, pk):
    try:
        user = User.objects.get(pk=pk)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)   

    profile = ProfileModel.objects.get(user=user)
    profileSerializer = ProfileSerializer(profile)
    profileData = profileSerializer.data
    profileData['image'] =  settings.BASE_URL + profileData['image']
    profileData['email'] = user.email
    posts = PostsModel.objects.filter(user=user, group=False)
    postSerializer = PostsSerializer(posts, many=True)
    postJson = postSerializer.data
    postJson.reverse()
    for post in postJson:
        user = User.objects.get(pk=int(post['user']))
        prof = ProfileModel.objects.get(user=user)
        post['user'] = {"image":settings.BASE_URL+prof.image.url, "name":prof.name, "id": post['user']}
        likes = []
        boolValue = False
        for id in post['likes']:
            print(id)
            print(pk)
            if int(pk) == id:
                boolValue = True
            user = User.objects.get(pk=id)
            prof = ProfileModel.objects.get(user=user)
            likes.append({"image":settings.BASE_URL+prof.image.url,"name":prof.name, "id": id})
        post['likes'] = likes
        if boolValue:
            post['liked'] = True
        else:
            post['liked'] = False
        comments = []
        commentsReverse = post['comments']
        # reversed(commentsReverse)
        commentsReverse.reverse()
        for id in commentsReverse:
            comment = CommentModel.objects.get(pk=id)
            user = comment.user
            text = comment.text
            prof = ProfileModel.objects.get(user=user)
            comments.append({"image":settings.BASE_URL+prof.image.url,"name":prof.name, "id": user.id, "text":text})
        post['comments'] = comments
    return Response({"profile":profileData,"post":postJson}, status=status.HTTP_200_OK)
  

class MyFriendsView(APIView):
  # get my friends
  def get(self, request):
    try:
        token = request.META.get('HTTP_AUTHORIZATION', '')
        token = token.split(" ")[1]
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
            friends = FriendshipModel.objects.get(user=user)
            serializer = FriendshipSerializer(friends)
            data = serializer.data
            friends = []
            for id in data['friendsList']:
              user = User.objects.get(pk=id)
              prof = ProfileModel.objects.get(user=user)
              friends.append({"image":settings.BASE_URL+prof.image.url,"name":prof.name, "id": id})
            data['friendsList'] = friends
            return Response(data, status=status.HTTP_200_OK)


class AllFriendsView(APIView):
  # get my friend friends
  def get(self, request, pk):
    try:
        token = request.META.get('HTTP_AUTHORIZATION', '')
        token = token.split(" ")[1]
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
            user = User.objects.get(pk=pk)
            friends = FriendshipModel.objects.get(user=user)
            serializer = FriendshipSerializer(friends)
            data = serializer.data
            friends = []
            for id in data['friendsList']:
              user = User.objects.get(pk=id)
              friends.append({"name":ProfileModel.objects.get(user=user).name, "id": id})
            data['friendsList'] = friends
            return Response(data, status=status.HTTP_200_OK)


class PeopleView(APIView):
  # add friend
  def get(self, request, pk):
    try:
        token = request.META.get('HTTP_AUTHORIZATION', '')
        token = token.split(" ")[1]
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
            friends = FriendshipModel.objects.get(user=user)
            userAdd = User.objects.get(pk=pk)
            friends.friendsList.add(userAdd)
            friends.save()

            friendsOther = FriendshipModel.objects.get(user=userAdd)
            friendsOther.friendsList.add(user)
            friendsOther.save()

            serializer = FriendshipSerializer(friends)
            data = serializer.data
            friends = []
            for id in data['friendsList']:
              user = User.objects.get(pk=id)
              friends.append({"name":ProfileModel.objects.get(user=user).name, "id": id})
            data['friendsList'] = friends
            return Response(data, status=status.HTTP_200_OK)
  
  # unfriend
  def delete(self, request, pk):
    try:
        token = request.META.get('HTTP_AUTHORIZATION', '')
        token = token.split(" ")[1]
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
            friends = FriendshipModel.objects.get(user=user)
            userRemove = User.objects.get(pk=pk)
            friends.friendsList.remove(userRemove)
            friends.save()

            friendsOther = FriendshipModel.objects.get(user=userRemove)
            friendsOther.friendsList.remove(user)
            friendsOther.save()

            serializer = FriendshipSerializer(friends)
            data = serializer.data
            friends = []
            for id in data['friendsList']:
              user = User.objects.get(pk=id)
              friends.append({"name":ProfileModel.objects.get(user=user).name, "id": id})
            data['friendsList'] = friends
            return Response(data, status=status.HTTP_200_OK)


class searchPeople(APIView):
  # seach for people
  def get(self, request, value):
    try:
        token = request.META.get('HTTP_AUTHORIZATION', '')
        token = token.split(" ")[1]
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
            profiles = ProfileModel.objects.exclude(user=user).filter(Q(name__contains=value) | Q(mobile__contains=value))
            serializer = ProfileSerializer2(profiles, many=True)
            friends = FriendshipModel.objects.get(user=user)
            serializerFriends = FriendshipSerializer(friends).data
            friends = serializerFriends['friendsList']
            i = 0
            for pk in friends:
                userFriend = User.objects.get(pk=pk)
                print(ProfileModel.objects.get(user=userFriend).pk)
                friends[i] = ProfileModel.objects.get(user=userFriend).pk
                i = i + 1
            print(friends)
            json = serializer.data
            for profile in json:
                profile["image"] = settings.BASE_URL + profile["image"]
                us = User.objects.get(profile__pk = profile['pk'])
                profile["email"] = us.username
                profile["userPk"] = us.pk
                try:
                    friends.index(profile['pk'])
                    profile["friend"] = True
                except:
                    profile["friend"] = False
            return Response(json, status=status.HTTP_200_OK)


class FriednsRepresentation(APIView):
    def get(self, request):
        nodes = []
        edges = []

        users = []
        profiles = ProfileModel.objects.all()
        for profile in profiles:
            Profile = ProfileSerializer(profile)
            friends = FriendshipModel.objects.get(user = profile.user)
            serializer = FriendshipSerializer(friends)
            friendsList = serializer.data['friendsList']
            data = {}
            data["name"] = profile.name
            data["image"] = profile.image.url
            data["id"] = profile.user.id
            data["friendsList"] = friendsList
            users.append(data)
        for profile in users:
            nodes.append({ "id": profile["id"], "label": profile["name"], "image": settings.BASE_URL+profile["image"], "shape": 'image' })
            for user in profile["friendsList"]:
                # edges.append({ from: profile.user.id, to: user.id, length: 150 })
                edges.append({ "from":profile["id"], "to": user, "length": 200 })

                num = my_search(user, users, 'id')
                if num > -1:
                    users[num]["friendsList"].remove(profile["id"])
                    print(users)

        return Response({"nodes":nodes,"edges":edges}, status=status.HTTP_200_OK)


def binary_search(number, array, key, lo, hi):
    if hi < lo: return -1       # no more numbers
    mid = (lo + hi) // 2        # midpoint in array
    if number == array[mid][key]:
        return mid                  # number found here
    elif number < array[mid][key]:
        return binary_search(number, array, key, lo, mid - 1)     # try left of here
    else:
        return binary_search(number, array, key, mid + 1, hi)     # try above here
 
def my_search(num, array, key):
    return binary_search(num, array, key, 0, len(array) - 1)

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
  

