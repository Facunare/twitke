from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from . import forms
from .models import Tweet
from profiles.models import Profiles
# Create your views here.


# 2. Profiles (in process).

# 3. Retweet

# 4. Trends

# 5. Despues de registrarte tener la posibilidad de modificar tu arroba, foto de perfil, biografia, etc.

# 6. Function for the post of tweets. (add images, emojis, self location, pools)

# 7. Keep tweets. ("guardados section")

# 8. Admin view (Data analytics, moderate content (ban and delete accounts and tweets that are breaking the rules ))

# 9. messenger (lo menos probable que haga)

# 10. Ajax en botones

# 11. Buscar usuarios en el buscador

# Errores boludos:
# 2. Arreglar cuando se crea un usuario con gmail.
# 3. Que se pueda seleccionar el texto del tweet

def globalFeed(request):
    tweets = Tweet.objects.all().filter(parent_tweet = None)
    
    return render(request, 'globalFeed.html',{
            'form': forms.postTweet,
            'tweets': tweets
    })

@login_required
def postTweet(request):
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
    
    if search:
        tweets = Tweet.objects.filter(content__icontains = search)
        if tweets.count() == 0:
             return render(request, 'globalFeed.html',{
                'error': True
            })

    return render(request, 'globalFeed.html',{
        'tweets': tweets
    })