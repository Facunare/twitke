from django.urls import path, include
from . import views

urlpatterns = [

    path('', views.globalFeed, name='globalFeed'),
    path('tweet/', views.postTweet, name="postTweet"),
    path('tweet/response/<int:id>', views.responseTweet, name="responseTweet"),
    path('tweet/detail/<int:id>', views.tweetDetails, name="tweetDetails"),
    path('like/<int:id>', views.like, name="like"),
    path('like/<int:id>/delete', views.deleteTweet, name="deleteTweet"),
    path('search/', views.searchTweet, name="search"),
    path('keep/<int:tweetId>', views.keepTweets, name="keepTweets"),
    path('keepTweets/<int:id>', views.keeped, name="keeped"),
    path('update/tweet/<int:id>', views.updateTweet, name="updateTweet"),
    path('retweet/<int:id>', views.retweet, name="retweet"),
    path("verificate/", views.verificate, name="verificate"),
    path('verificate/user/<int:id>', views.verificateUser, name="verificateUser"),
    path('banned/', views.banned, name='banned'),
    path('unban/', views.unban, name='unban'),
    path('unban/user/<int:id>', views.unbanUser, name="unbanUser"),
    path('deleteUnbanRequest/<int:id>/delete,', views.deleteUnbanRequest, name="deleteUnbanRequest"),
]