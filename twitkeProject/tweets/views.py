from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from . import forms
from django.http import JsonResponse
from .models import Tweet
from profiles.models import Profiles
from tweet_profiles.models import Tweet_profile
# Create your views here.



# 1. Retweet

# 2. Function for the post of tweets. (add images, emojis, videos)

# 3. Admin view (verificate accounts, Data analytics, moderate content (ban and delete accounts and tweets that are breaking the rules ))

# 4. Profile sections (answers, retweets, etc).

# 5. IA 

# 6. Twitter design

# 7. Ver lo que retwiteen o lo que le dan like los que sigo.


# Errores boludos:
# 1. Arreglar gmail.

def globalFeed(request):
    tweets = Tweet_profile.objects.all().filter(tweet__parent_tweet = None)
    
    return render(request, 'globalFeed.html',{
            'form': forms.postTweet,
            'tweets': tweets,        
    })
    

@login_required
def like(request, id):
    try:
        tweet = Tweet.objects.get(id=id)
        user = request.user
        if user not in tweet.likes_users.all():
            tweet.likes += 1
            tweet.likes_users.add(user)
            tweet.save()
            is_liked = True
        else:
            tweet.likes -= 1
            tweet.likes_users.remove(user)
            tweet.save()
            is_liked = False
        return JsonResponse({'is_liked': is_liked, 'likes': tweet.likes, 'id': id})
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
        Tweet_profile.objects.create(tweet = tweet, profile = current_profile)
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
    return render(request, 'tweetDetail.html',{
        'tweets': tweet,
        'parent_tweet': parent_tweet,
        'profile': profile
    })
    


def searchTweet(request):
    search = request.GET.get("search")
    tweets = ""
    profiles= ""
    current_profile = Profiles.objects.get(user=request.user)
    if search:
        tweets = Tweet.objects.filter(content__icontains = search)
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
    tweet = Tweet.objects.get(id=tweetId)
    profile = Profiles.objects.get(user=request.user)

    if tweet in profile.keeps.all():
        profile.keeps.remove(tweet)
        kept = False
    else:
        profile.keeps.add(tweet) 
        kept = True
    
    
    
    return JsonResponse({'is_kept': kept, 'id': tweetId})
@login_required    
def keeped(request, id):
    profile = Profiles.objects.get(id=id)
    keptTweets = profile.keeps.all()
    return render(request, 'keptTweets.html', {
        'keeps': keptTweets,
        'profile': profile
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
    tweet_to_retweet = Tweet.objects.get(id = id)
    current_profile = Profiles.objects.get(user__username = request.user.username)
    tweet = Tweet.objects.create(user = tweet_to_retweet.user, content = tweet_to_retweet.content, is_retwitted = True)
    Tweet_profile.objects.create(tweet = tweet, profile = current_profile)
    return redirect('/')