from django.shortcuts import render, get_object_or_404, redirect    
from django.contrib.auth.models import User
from .models import Profiles, Tweet
# Create your views here.

def myProfile(request, account):
    
    
    user = Profiles.objects.get(username=account)
    followers = user.followers_users.all()
    
    cant_followers = int(user.followers)
    tweets = Tweet.objects.filter(user__username=account).all()
    return render(request, 'myProfile.html', {
        'usuario': user,
        'is_self': request.user.is_authenticated and request.user.username == account,
        'followers': followers,
        'cant_followers': cant_followers,
        'tweets': tweets
    })
    
def follow(request, id):
    profile = Profiles.objects.get(id=id)
    user = request.user
    if user in profile.followers_users.all():
        profile.followers_users.remove(request.user)      
        profile.followers -= 1
        profile.save()
        followed = False
    else:
        profile.followers_users.add(request.user)
        profile.followers += 1
        profile.save()
        followed = True

    return_url = request.GET.get('return_url')
    if return_url:
        return redirect(return_url)
    return redirect('myProfile', id=id, followed=followed)