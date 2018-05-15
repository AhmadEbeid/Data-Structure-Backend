"""BackEnd URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from socialNetwork import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^signIn/$', views.SignInView.as_view()),
    url(r'^signUp/$', views.SignUpView.as_view()),
    url(r'^myPostsView/$', views.MyPostsView.as_view()),
    url(r'^postView/(?P<pk>[0-9]+)/$', views.postGetView.as_view()),
    url(r'^userProfile/(?P<pk>[0-9]+)/$', views.userProfilePageView.as_view()),
    url(r'^friends/$', views.MyFriendsView.as_view()),
    url(r'^people/(?P<pk>[0-9]+)/$', views.PeopleView.as_view()),
    url(r'^search/(?P<value>[\w\-]+)/$', views.searchPeople.as_view()),
    url(r'^friendsOfFriend/(?P<pk>[0-9]+)/$', views.AllFriendsView.as_view()),
    url(r'^FriednsRepresentation/$', views.FriednsRepresentation.as_view()),
]
