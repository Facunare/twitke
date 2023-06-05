import email
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from profiles.models import Profiles
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from profiles.models import Profiles
import requests
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

@login_required
def signup_google(request):
    
    social_account = SocialAccount.objects.get(user=request.user, provider='google')
    extra_data = social_account.extra_data
    username = extra_data.get('name', '')
    avatar_url = extra_data.get('picture', '')
    try:
        profile = Profiles.objects.get(id = request.user.id)
        print("hola")
    
        return render(request, 'globalFeed.html')
        
    except:
        print("chau")
        response = requests.get(avatar_url)
        if response.status_code == 200:
            image_file = ContentFile(response.content)
            file_name = f"profile_{request.user.id}.png"
            file_path = default_storage.save(f"profileImages/{file_name}", image_file)
            
        
        profile = Profiles.objects.create(id=request.user.id, user=request.user, username=username, profileImage = file_path)
        profile.save()
        return render(request, 'globalFeed.html')


def signup(request):
    
    if request.method == 'GET':
        return render(request, 'signup.html',{
            'form' : UserCreationForm
        })
    else:
        
        if request.POST['password1'] == request.POST['password2']:
            try:
                
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'], email=request.POST['email'])
                user.save()
                
                try:
                    Profiles.objects.create(id = user.id, user = user, username = user.username)
                except Exception as e:
                    print(e)
                    
                
                return redirect('/signin/')
            except:
                
                return render(request, 'signup.html',{
                    'form' : UserCreationForm,
                    'error': 'Usuario existente'
                })
        else:
            return render(request, 'signup.html',{
                'form' : UserCreationForm,
                'error': 'Las contraseñas no coinciden'
            })

@login_required
def signout(request):
    logout(request)
    return redirect('/')


def signin(request):
    if request.method == 'GET':

        return render(request, 'signin.html',{
            'form': AuthenticationForm
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:

            return render(request, 'signin.html',{
                'form': AuthenticationForm,
                'error': "El usuario o contraseña es incorrecto"
            })
        else:
            login(request, user)
            return redirect('globalFeed')
        
def landingPage(request):
    return render(request, 'landingPage.html')

def change(request):
    return render(request, 'signin.html')