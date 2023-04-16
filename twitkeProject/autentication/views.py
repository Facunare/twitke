from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from profiles.models import Profiles
# Create your views here.

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html',{
            'form' : UserCreationForm
        })
    else:
        
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
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