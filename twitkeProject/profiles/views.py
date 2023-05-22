from django.shortcuts import render, get_object_or_404, redirect    
from django.contrib.auth.models import User
from .models import Profiles, Tweet, verfifyRequests
from datetime import datetime
from tweet_profiles.models import Tweet_profile
# Create your views here.
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


def myProfile(request, id):
    cant_followers = 0
    cant_following = 0
    myLikes = request.GET.get("myLikes")
    myTweets = request.GET.get("myTweets")
    user = Profiles.objects.get(id=id)
    followers = user.followers_users.all()
    following = user.followed_users.all()
    cant_following = user.followed_users.all().count()
    cant_followers = int(user.followers)
    cant_following = user.followed_users.all().count()
    solicitudes = verfifyRequests.objects.all()
    requested = False
    tweets = Tweet_profile.objects.filter(profile__user__id=id).all()
    if myLikes == "":
        tweetLIKE = user.like_tweets.all()
        tweets = Tweet_profile.objects.filter(tweet_id__in=[tweet.id for tweet in tweetLIKE])
    elif myTweets == "":
        tweets = Tweet_profile.objects.filter(profile__user__id=id).all()
    
    for soli in solicitudes:
        if soli.profile == user:
            requested = True
    return render(request, 'myProfile.html', {
        'usuario': user,
        'is_self': request.user.is_authenticated and request.user.id == id,
        'followers': followers,
        'cant_followers': cant_followers,
        'tweets': tweets,
        'cant_following': cant_following,
        'following': following,
        'solicitudes': solicitudes,
        'requested': requested,
    })
    
    
@login_required
def follow(request, id):
    profile = Profiles.objects.get(id=id)
    current_profile = Profiles.objects.get(user__username=request.user.username)
    print("Perfil", profile)
    print("User actual", current_profile)
    if current_profile in profile.followers_users.all():
        current_profile.followed_users.remove(profile)
        profile.followers_users.remove(current_profile)
        profile.followers -= 1
        follow = False
    else:
        current_profile.followed_users.add(profile)
        profile.followers_users.add(current_profile)
        profile.followers += 1
        follow = True
    profile.save()
    current_profile.save()


    return JsonResponse({'is_follow': follow, 'cant_followers': profile.followers})


@login_required
def updateProfile(request, id):
    used = False
    profile = Profiles.objects.get(id=id)
    profiles = Profiles.objects.all()
    if request.method == "POST":
        if request.POST['input-name']:
            print(request.POST['input-name'])
            for perfil in profiles:
                if perfil.username == str(request.POST['input-name']):
                    print('Ese nombre esta en uso')
                    used = True
                    return JsonResponse({'is_used': used})
                else:
                    profile.username = str(request.POST['input-name'])
                    
                
                    
        if request.POST['input-biography']:
            profile.biography = str(request.POST['input-biography'])
        
        if request.FILES.get('input-photo'):
            profile.profileImage = request.FILES['input-photo']
            
        if request.FILES.get('input-banner'):
            profile.profileBanner= request.FILES['input-banner']
            
        if request.POST['webSite']:
            profile.webSite = request.POST['webSite']
        birthday_str = request.POST.get('birthday')
        if birthday_str:    
            birthday = datetime.strptime(birthday_str, '%Y-%m-%d').date()
            profile.birthday = birthday
        
        
    profile.save()    
    
    return JsonResponse({'is_used': used})

@login_required
def verifyRequest(request, id):
    profile = Profiles.objects.get(id = id)
    verfifyRequests.objects.create(profile = profile)
    return_url = request.GET.get('return_url')
    if return_url:
        return redirect(return_url)
    return redirect('myProfile', id=id)

@login_required
def deleteVerifyRequest(request, id):
    verify_req = verfifyRequests.objects.get(profile_id = id)
    verify_req.delete()
    return redirect('verificate')
    