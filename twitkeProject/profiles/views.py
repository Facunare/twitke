from django.shortcuts import render, get_object_or_404, redirect    
from django.contrib.auth.models import User
from .models import Profiles, Tweet
# Create your views here.

def myProfile(request, account):
    cant_followers = 0
    cant_following = 0
    current_profile = ""
    current_profile = Profiles.objects.get(user__username = request.user.username)
    if request.user.is_authenticated and request.user.username == account:
        current_profile = Profiles.objects.get(user__username = request.user.username)
    user = Profiles.objects.get(username=account)
    followers = user.followers_users.all()
    following = user.followed_users.all()
    # if request.user.is_authenticated and request.user.username == account:
    #     current_profile = Profiles.objects.get(user__username = request.user.username)
    #     cant_followers = int(current_profile.followers)
    #     cant_following = current_profile.followed_users.all().count()
    
    cant_following = user.followed_users.all().count()
    cant_followers = int(user.followers)
    tweets = Tweet.objects.filter(user__username=account).all()
    print(cant_followers)
    print(cant_following)
    cant_following = user.followed_users.all().count()
    return render(request, 'myProfile.html', {
        'usuario': user,
        'current_user': current_profile,
        'is_self': request.user.is_authenticated and request.user.username == account,
        'followers': followers,
        'cant_followers': cant_followers,
        'tweets': tweets,
        'cant_following': cant_following,
        'following': following
    })
    
def follow(request, id):
    profile = Profiles.objects.get(id=id)
    current_profile = Profiles.objects.get(user__username=request.user.username)
    
    if current_profile in profile.followers_users.all():
        current_profile.followed_users.remove(profile)
        profile.followers_users.remove(current_profile)
        profile.followers -= 1
    else:
        current_profile.followed_users.add(profile)
        profile.followers_users.add(current_profile)
        profile.followers += 1
    
    profile.save()
    current_profile.save()


    return_url = request.GET.get('return_url')
    if return_url:
        return redirect(return_url)
    return redirect('myProfile', id=id)