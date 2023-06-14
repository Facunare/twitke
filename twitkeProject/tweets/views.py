from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from . import forms
from django.http import JsonResponse
from .models import Tweet, TweetImage
from profiles.models import Profiles, verfifyRequests, unbanRequests
from tweet_profiles.models import Tweet_profile
from django.db.models import Q
from insult_detection.insult_detection import InsultDetector

def globalFeed(request):
    
    current_profile = ""
    search = request.GET.get("searchUser")
    foryou = request.GET.get("foryou")
 
    images = TweetImage.objects.all()
    if search:
        users = Profiles.objects.filter(username__icontains = search).all()
    else:
        users = Profiles.objects.all()
    if request.user.is_authenticated:
        current_profile = Profiles.objects.get(user__username = request.user.username)
        if current_profile.banned:
            return redirect('banned')
        followers = current_profile.followed_users.all()
        tweets = Tweet_profile.objects.filter(Q(profile__in=followers) | Q(retwitted_by__in = followers) | Q(profile=current_profile),  parent_tweet=None)
        
    else:
        tweets = Tweet_profile.objects.all().filter(parent_tweet = None)

    if str(foryou) == "":
        tweets = Tweet_profile.objects.all().filter(parent_tweet = None)
        
    context = {
        'form': forms.postTweet,
        'tweets': tweets,        
        'users': users,
        'images': images
    }
    
    return render(request, 'globalFeed.html',context)
    
@login_required
def retweet(request, id):
    tweet= Tweet.objects.get(id=id)
    tweet_to_retweet = Tweet_profile.objects.get(tweet = tweet)
    current_profile = Profiles.objects.get(user__username=request.user.username)

    if tweet_to_retweet.tweet in current_profile.retweets.all():
        current_profile.retweets.remove(tweet_to_retweet.tweet)
        tweet_to_retweet.retwitted_by.remove(current_profile)
        is_retwitted = False
    else:
        current_profile.retweets.add(tweet_to_retweet.tweet)
        tweet_to_retweet.retwitted_by.add(current_profile)   
        is_retwitted = True    
    retweets = tweet_to_retweet.retwitted_by.all().count()
    return JsonResponse({'is_retwitted': is_retwitted, 'retweets': retweets, 'id': id, "darkMode": current_profile.darkMode})

@login_required
def like(request, id):
    try:
        tweet = Tweet_profile.objects.get(tweet_id=id)
        
        if request.user.is_authenticated:
            current_profile = Profiles.objects.get(user__username = request.user.username)
            
        if current_profile not in tweet.likes_users.all():
            tweet.likes_users.add(current_profile)
            current_profile.like_tweets.add(tweet.tweet)
            tweet.save()
            current_profile.save()
            is_liked = True
        else:
            tweet.likes_users.remove(current_profile)
            current_profile.like_tweets.remove(tweet.tweet)
            tweet.save()
            current_profile.save()
            is_liked = False
        likes = tweet.likes_users.all().count()
        return JsonResponse({'is_liked': is_liked, 'likes': likes, 'id': id, "darkMode": current_profile.darkMode})
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
        detector = InsultDetector(model_path='insult_detection/model.h5', tokenizer_path='insult_detection/tokenizer.json', max_seq_length=5)
        is_insult = detector.classify_text(request.POST['content'])
        if is_insult >= 0.5:
             current_profile.strikes -= 1
             current_profile.save()
             if current_profile.strikes <= 0:
                 current_profile.banned = True
                 current_profile.save()
             return render(request, 'insultDetected.html')
        else:
            tweet = Tweet.objects.create(user = request.user, content = request.POST['content'])
            for media in request.FILES.getlist('tweetImage'):
                contenido = media.read().decode('latin-1')
                if contenido[-3:] == "100":
                    TweetImage.objects.create(tweet=tweet, video=media)
                else:
                    TweetImage.objects.create(tweet=tweet, image=media)
            if request.FILES.getlist('tweetImage'):
                Tweet_profile.objects.create(tweet = tweet, profile = current_profile, haveMultimedia = True)
            else:
                Tweet_profile.objects.create(tweet = tweet, profile = current_profile)
            return redirect('/')
    
@login_required
def responseTweet(request, id):
    current_profile = Profiles.objects.get(user__username = request.user.username)
    tweetOriginal = Tweet_profile.objects.get(tweet_id = id)
    if request.method == "POST":
        detector = InsultDetector(model_path='insult_detection/model.h5', tokenizer_path='insult_detection/tokenizer.json', max_seq_length=5)
        is_insult = detector.classify_text(request.POST['contentResponse'])
        if is_insult >= 0.5:
             current_profile.strikes -= 1
             current_profile.save()
             if current_profile.strikes <= 0:
                 current_profile.banned = True
                 current_profile.save()
             return render(request, 'insultDetected.html')
        else:            
            tweet = Tweet.objects.create(user = request.user, content = request.POST['contentResponse'])
            Tweet_profile.objects.create(tweet = tweet, profile = current_profile, parent_tweet = tweetOriginal)
            tweetOriginal.tweet.responses += 1
            tweetOriginal.save()
            tweetOriginal.tweet.save()
            return redirect(f'/tweet/detail/{id}')
    

def tweetDetails(request, id):
    parent_tweet = Tweet_profile.objects.get(tweet__id = id)
    tweet = Tweet_profile.objects.all().filter(parent_tweet= parent_tweet)
    print(parent_tweet)
    profile = Profiles.objects.get(id=parent_tweet.profile.user.id)
    likes = parent_tweet.likes_users.all()
    return render(request, 'tweetDetail.html',{
        'tweets': tweet,
        'parent_tweet': parent_tweet,
        'profile': profile,
        'likes': likes,
        'is_self': request.user.is_authenticated and request.user.id == id
    })
    


def searchTweet(request):
    search = request.GET.get("search")
    tweets = ""
    profiles= ""
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
        'buscado': True
      
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



from django.contrib.auth.models import User

@staff_member_required
def verificate(request):
    searchUsers = request.GET.get("searchUsers")
    if searchUsers:
        users = verfifyRequests.objects.filter(profile__atName__icontains = searchUsers).all()
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

@staff_member_required
def unbanUser(request, id):   
    user = Profiles.objects.get(id = id)
    if user.banned:
        user.banned = False
        user.strikes = 3
        unban_req = unbanRequests.objects.get(profile_id = id)
        unban_req.delete()
    else:
        user.banned = True
    user.save()
    return redirect('unban')


@staff_member_required
def unban(request):
    searchUsers = request.GET.get("searchUsers")
    if searchUsers:
        users = unbanRequests.objects.filter(profile__atName__icontains = searchUsers).all()
    else:
        users = unbanRequests.objects.all()
    return render(request, 'unban.html',{
        'users': users
    })
    
@login_required
def deleteUnbanRequest(request, id):
    unban_req = unbanRequests.objects.get(profile_id = id)
    unban_req.delete()
    return redirect('unban')

@login_required
def unbanRequest(request, id):
    profile = Profiles.objects.get(id = id)
    unbanRequests.objects.create(profile = profile, reason = request.POST['reason'])
    return_url = request.GET.get('return_url')
    if return_url:
        return redirect(return_url)
    return redirect('myProfile', id=id)

def banned(request):
    solicitudes = unbanRequests.objects.all()
    requested = False
    current_profile = Profiles.objects.get(user__username=request.user.username)
    for soli in solicitudes:
        if soli.profile == current_profile:
            requested = True
        else:
            requested = False
    print(requested)
    return render(request, 'banned.html',{
        'requested': requested,
    })