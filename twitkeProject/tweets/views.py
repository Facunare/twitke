from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from . import forms
from .models import Tweet
from profiles.models import Profiles
# Create your views here.


# 1. Profiles (in process).

# 2. Retweet

# 3. Despues de registrarte tener la posibilidad de modificar tu arroba, foto de perfil, biografia, etc.

# 4. Function for the post of tweets. (add images, emojis, self location, pools)

# 5. Admin view (Data analytics, moderate content (ban and delete accounts and tweets that are breaking the rules ))

# 6. Ajax en botones

# 7. Buscar usuarios en el buscador, y en los seguidos y seguidores.

# 8. Edit tweets

# 9. Tweet design

# Errores boludos:
# 1. Arreglar cuando se crea un usuario con gmail.
# 2. Lo del texto del tweet


def globalFeed(request):
    profile = None
    tweets = Tweet.objects.all().filter(parent_tweet = None)
    if request.user.is_authenticated:
        profile = Profiles.objects.get(user=request.user)
    return render(request, 'globalFeed.html',{
            'form': forms.postTweet,
            'tweets': tweets,
            'profile': profile
    })

@login_required
def postTweet(request):

    current_profile = Profiles.objects.get(user__username = request.user.username)
    if request.method == 'GET':
        return render(request, 'globalFeed.html',{
            'form': forms.postTweet
        })
    else:
        Tweet.objects.create(user = request.user, content = request.POST['content'])
        return redirect('/')

@login_required
def like(request, id):
    tweet = Tweet.objects.get(id = id)
    user = request.user
    if user not in tweet.likes_users.all():
        tweet.likes += 1
        tweet.likes_users.add(user)
        tweet.save()
    else:
        tweet.likes -= 1
        tweet.likes_users.remove(user)
        tweet.save()
    
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def deleteTweet(request, id):
    tweet = Tweet.objects.get(id = id)
    tweet.delete()
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def responseTweet(request, id):
    if request.method == "POST":
        print(id)
        Tweet.objects.create(user = request.user, content = request.POST['contentResponse'], parent_tweet = id)
        return redirect(f'/tweet/detail/{id}')
    

def tweetDetails(request, id):
    tweet = Tweet.objects.all().filter(parent_tweet = id)
    parent_tweet = Tweet.objects.get(id = id)
    profile = Profiles.objects.get(username=parent_tweet.user.username)
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
    
    
    
    return redirect(request.META.get('HTTP_REFERER', '/'), {'kept': kept})
@login_required    
def keeped(request, account):
    profile = Profiles.objects.get(username=account)
    keptTweets = profile.keeps.all()
    return render(request, 'keptTweets.html', {
        'keeps': keptTweets,
        'profile': profile
    })