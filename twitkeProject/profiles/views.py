from django.shortcuts import render, get_object_or_404, redirect    
from django.contrib.auth.models import User
from .models import Profiles, Tweet
# Create your views here.

def myProfile(request, account):
    
    current_profile = ""
    user = Profiles.objects.get(username=account)
    followers = user.followers_users.all()
    following = user.followed_users.all()
    if request.user.is_authenticated and request.user.username == account:
        current_profile = Profiles.objects.get(user__username = request.user.username)
    else:
        print(1)
    cant_followers = int(user.followers)
    tweets = Tweet.objects.filter(user__username=account).all()
    cant_following = user.followed_users.all().count()
    print(cant_following)
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
    current_profile = Profiles.objects.get(user__username = request.user.username)
    if current_profile in profile.followers_users.all():
        profile.followers_users.remove(current_profile)      
        profile.followers -= 1
        profile.save()
        followed = False
    else:
        profile.followers_users.add(current_profile)
        profile.followers += 1
        profile.save()
        followed = True
    if profile in current_profile.followed_users.all():
        current_profile.followed_users.remove(profile)
    else:
        current_profile.followed_users.add(profile)


    return_url = request.GET.get('return_url')
    if return_url:
        return redirect(return_url)
    return redirect('myProfile', id=id, followed=followed)