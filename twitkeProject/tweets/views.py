from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from . import forms
from django.http import JsonResponse
from .models import Tweet, TweetImage
from profiles.models import Profiles, verfifyRequests
from tweet_profiles.models import Tweet_profile
from django.db.models import Q
from django.contrib import messages
from datetime import datetime
from django.utils import timezone
from datetime import timedelta
# Create your views here.



# 1. Retweet

# 2. Functions for the post of tweets. (add images, emojis, videos)

# 3. IA 

# 4. Cambiar contraseña.

# 5. Ver usuarios que likearon




# Errores a solucionar:
# 1. Repensar el tema de los likes y keeps tweets con respecto de la tabla intermedia Tweet_profiles
# 2. Que quede guardado el color rojo del like



def globalFeed(request):
    current_profile = ""
    search = request.GET.get("searchUser")
    images = TweetImage.objects.all()
    if search:
        users = Profiles.objects.filter(username__icontains = search).all()
    else:
        users = Profiles.objects.all()
    if request.user.is_authenticated:
        current_profile = Profiles.objects.get(user__username = request.user.username)
        followers = current_profile.followed_users.all()
        tweets = Tweet_profile.objects.filter(Q(profile__in=followers) | Q(profile=current_profile), tweet__parent_tweet=None)
    else:
        tweets = Tweet_profile.objects.all().filter(tweet__parent_tweet = None)
    return render(request, 'globalFeed.html',{
            'form': forms.postTweet,
            'tweets': tweets,        
            'current_profile': current_profile,
            'users': users,
            'images': images
    })
    

@login_required
def like(request, id):
    try:
        tweet = Tweet_profile.objects.get(tweet_id=id)
        
        if request.user.is_authenticated:
            current_profile = Profiles.objects.get(user__username = request.user.username)
            
        if current_profile not in tweet.likes_users.all():
            tweet.likes_users.add(current_profile)
            tweet.save()
            is_liked = True
        else:
            tweet.likes_users.remove(current_profile)
            tweet.save()
            is_liked = False
        likes = tweet.likes_users.all().count()
        return JsonResponse({'is_liked': is_liked, 'likes': likes, 'id': id})
    except Exception as e:
        print(f"Error: {e}")
        return JsonResponse({'error': str(e)})

@login_required
def deleteTweet(request, id):
    print(id)
    tweet = Tweet.objects.get(id = id)
    tweet.delete()
    return redirect('globalFeed')

@login_required
def postTweet(request):

    current_profile = Profiles.objects.get(user__username = request.user.username)
    if request.method == 'GET':
        return render(request, 'globalFeed.html',{
            'form': forms.postTweet
        })
    else:
        
        tweet = Tweet.objects.create(user = request.user, content = request.POST['content'])
        for image in request.FILES.getlist('tweetImage'):
            TweetImage.objects.create(tweet=tweet, image=image)
        Tweet_profile.objects.create(tweet = tweet, profile = current_profile, images = request.FILES.getlist('tweetImage'))
        return redirect('/')
    
@login_required
def responseTweet(request, id):
    current_profile = Profiles.objects.get(user__username = request.user.username)
    if request.method == "POST":
        tweet = Tweet.objects.create(user = request.user, content = request.POST['contentResponse'], parent_tweet = id)
        Tweet_profile.objects.create(tweet = tweet, profile = current_profile)
        return redirect(f'/tweet/detail/{id}')
    

def tweetDetails(request, id):
    tweet = Tweet_profile.objects.all().filter(tweet__parent_tweet = id)
    parent_tweet = Tweet_profile.objects.get(tweet_id = id)
    profile = Profiles.objects.get(id=parent_tweet.profile.user.id)
    print(parent_tweet.likes_users.all().count())
    return render(request, 'tweetDetail.html',{
        'tweets': tweet,
        'parent_tweet': parent_tweet,
        'profile': profile
    })
    


def searchTweet(request):
    search = request.GET.get("search")
    tweets = ""
    profiles= ""
    current_profile = ""
    if request.user.is_authenticated:
        current_profile = Profiles.objects.get(user__username = request.user.username)
    if search:
        tweets = Tweet_profile.objects.filter(tweet__content__icontains = search)
        profiles = Profiles.objects.filter(user__username__icontains = search)
        if tweets.count() == 0 and profiles.count() == 0:
             return render(request, 'globalFeed.html',{
                'error': True
            })

    return render(request, 'globalFeed.html',{
        'tweets': tweets,
        'profilesSearched': profiles,
        'current_profile': current_profile
    })

@login_required
def keepTweets(request, tweetId):
    tweet = Tweet_profile.objects.get(tweet_id=tweetId)
    profile = Profiles.objects.get(user=request.user)

    if tweet.tweet in profile.keeps.all():
        profile.keeps.remove(tweet.tweet)
        kept = False
    else:
        profile.keeps.add(tweet.tweet) 
        kept = True
    
    
    
    return JsonResponse({'is_kept': kept, 'id': tweetId})
@login_required    
def keeped(request, id):
    current_profile = Profiles.objects.get(user__username = request.user.username)
    keeps = current_profile.keeps.all()
    tweets = Tweet_profile.objects.filter(tweet_id__in=[keep.id for keep in keeps])
    print(tweets)



    return render(request, 'keptTweets.html', {
        'keeps': tweets,
        'profile': current_profile
    })

@login_required
def updateTweet(request, id):
    tweet_to_update = Tweet.objects.get(id = id)
    if request.method == 'POST':      
        tweet_to_update.content = request.POST['content']
        tweet_to_update.edited = True
        tweet_to_update.save()
        return JsonResponse({'tweetContent': str(tweet_to_update.content), 'tweetId': id}) 
    
    
    return JsonResponse({'tweetContent': str(tweet_to_update.content), 'tweetId': id})

@login_required
def retweet(request, id):
   

    tweet= Tweet.objects.get(id=id)
    tweet_to_retweet = Tweet_profile.objects.get(tweet = tweet)
    current_profile = Profiles.objects.get(user__username=request.user.username)

    if tweet_to_retweet.tweet in current_profile.retweets.all():
        print("estoy")
        current_profile.retweets.remove(tweet_to_retweet.tweet)
        tweet_to_retweet.retwitted_by.remove(current_profile)
        tweet_to_delete = Tweet_profile.objects.get(tweet = tweet)
        tweet_to_delete.delete()
    else:
        print("no estoy")
        current_profile.retweets.add(tweet_to_retweet.tweet)
        tweet_to_retweet.retwitted_by.add(current_profile)       
        tweet = Tweet.objects.create(user = tweet_to_retweet.profile.user, content = tweet_to_retweet.tweet.content)
        Tweet_profile.objects.create(tweet = tweet, profile = current_profile)
    
    return redirect('/')


from django.contrib.auth.models import User

@staff_member_required
def verificate(request):
    searchUsers = request.GET.get("searchUsers")
    if searchUsers:
        users = verfifyRequests.objects.filter(profile__username__icontains = searchUsers).all()
    else:
        users = verfifyRequests.objects.all()
    return render(request, 'verificate.html',{
        'users': users
    })

    
@staff_member_required
def verificateUser(request, id):
    
    user = Profiles.objects.get(id = id)
    if user.is_verified:
        user.is_verified = False
    else:
        user.is_verified = True
    user.save()
    return redirect('verificate')