from django.shortcuts import render, get_object_or_404, redirect    
from django.contrib.auth.models import User
from .models import Profiles, Tweet
from datetime import datetime
# Create your views here.

def myProfile(request, id):
    cant_followers = 0
    cant_following = 0
    current_profile = ""
    
    current_profile = Profiles.objects.get(user__username = request.user.username)
    if request.user.is_authenticated and request.user.id == id:
        current_profile = Profiles.objects.get(user__username = request.user.username)
    user = Profiles.objects.get(id=id)
    followers = user.followers_users.all()
    following = user.followed_users.all()
    cant_following = user.followed_users.all().count()
    cant_followers = int(user.followers)
    tweets = Tweet.objects.filter(user__id=id).all()
    print(cant_followers)
    print(cant_following)
    cant_following = user.followed_users.all().count()
    return render(request, 'myProfile.html', {
        'usuario': user,
        'current_user': current_profile,
        'is_self': request.user.is_authenticated and request.user.id == id,
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


def updateProfile(request, id):
    
    profile = Profiles.objects.get(id=id)
    profiles = Profiles.objects.all()
    if request.POST['input-name']:
        for profile in profiles:
            if profile.username == str(request.POST['input-name']):
                print('Ese nombre esta en uso')
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
    return_url = request.GET.get('return_url')
    if return_url:
        return redirect(return_url)
    return redirect('myProfile', id=id)